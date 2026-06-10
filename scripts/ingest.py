"""Ingestion: data/raw/datasets.json -> data/processed/documents.jsonl."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import DOCUMENTS_JSONL, RAW_DATASETS  # noqa: E402


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def load_datasets(path: Path = RAW_DATASETS) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    datasets = data.get("datasets")
    if not isinstance(datasets, list):
        raise ValueError("datasets.json must contain a list field named 'datasets'")
    return datasets


def ingest_item(item: dict) -> dict:
    text = clean_text(str(item.get("text", "")))
    if not text:
        raise ValueError(f"Empty text in item {item!r}")
    return {
        "doc_id": str(item["id"]),
        "name": str(item.get("name") or item["id"]).strip(),
        "text": text,
        "source_file": str(item.get("source_file", RAW_DATASETS)),
        "source": str(item.get("source", "unknown")),
    }


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def run(input_path: Path = RAW_DATASETS, output_path: Path = DOCUMENTS_JSONL) -> int:
    if not input_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {input_path}")
    documents = [ingest_item(item) for item in load_datasets(input_path)]
    write_jsonl(documents, output_path)
    return len(documents)


def main() -> None:
    count = run()
    print(f"Written {count} documents -> {DOCUMENTS_JSONL}")


if __name__ == "__main__":
    main()
