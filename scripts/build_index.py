"""Build TF-IDF index: prepare -> ingest -> chunk -> fit -> save."""

from __future__ import annotations

import json
import pickle
import shutil
import sys
from pathlib import Path

import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from app.chunker import load_jsonl, run as chunk_run  # noqa: E402
from app.config import (  # noqa: E402
    CHUNKS_JSONL,
    DATA_INDEX,
    INDEX_CHUNKS_JSONL,
    MATRIX_NPZ,
    MIN_DATASET_RECORDS,
    RAW_DATASETS,
    VECTORIZER_PKL,
)
from ingest import run as ingest_run  # noqa: E402
from prepare_datasets import main as prepare_main  # noqa: E402


def raw_dataset_count() -> int:
    if not RAW_DATASETS.exists():
        return 0
    try:
        data = json.loads(RAW_DATASETS.read_text(encoding="utf-8"))
        return len(data.get("datasets", []))
    except Exception:
        return 0


def ensure_raw_dataset() -> None:
    count = raw_dataset_count()
    if count >= MIN_DATASET_RECORDS:
        return
    print(
        f"Raw dataset has {count} records. Preparing dataset from Python standard library "
        f"to reach {MIN_DATASET_RECORDS}+ records..."
    )
    prepare_main()


def build_tfidf(texts: list[str]) -> tuple[TfidfVectorizer, scipy.sparse.csr_matrix]:
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
    )
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix


def save_index(vectorizer: TfidfVectorizer, matrix: scipy.sparse.csr_matrix) -> None:
    DATA_INDEX.mkdir(parents=True, exist_ok=True)
    with VECTORIZER_PKL.open("wb") as file:
        pickle.dump(vectorizer, file)
    scipy.sparse.save_npz(MATRIX_NPZ, matrix)
    shutil.copy2(CHUNKS_JSONL, INDEX_CHUNKS_JSONL)


def run() -> int:
    ensure_raw_dataset()
    doc_count = ingest_run()
    chunk_count = chunk_run()
    chunks = load_jsonl(CHUNKS_JSONL)
    texts = [chunk["text"] for chunk in chunks]
    if not texts:
        raise ValueError("No chunks to index")
    vectorizer, matrix = build_tfidf(texts)
    save_index(vectorizer, matrix)
    print(f"Documents: {doc_count}; chunks: {chunk_count}; matrix: {matrix.shape}")
    print(f"Index saved -> {DATA_INDEX}")
    return chunk_count


def main() -> None:
    run()


if __name__ == "__main__":
    main()
