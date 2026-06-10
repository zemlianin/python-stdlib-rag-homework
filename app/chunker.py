"""Chunking utilities: documents.jsonl -> chunks.jsonl."""

from __future__ import annotations

import json
from pathlib import Path

from app.config import CHUNK_MAX_CHARS, CHUNK_OVERLAP, CHUNKS_JSONL, DOCUMENTS_JSONL


def split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in text.split("\n\n") if part.strip()]


def split_long_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    parts: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        parts.append(text[start:end])
        start = end
    return parts


def apply_overlap(chunks: list[str], overlap: int, max_chars: int) -> list[str]:
    if overlap <= 0 or len(chunks) <= 1:
        return chunks
    result = [chunks[0]]
    for i in range(1, len(chunks)):
        prefix = result[-1][-overlap:]
        available = max_chars - len(prefix)
        result.append((prefix + chunks[i][:available]).strip())
    return result


def chunk_text(text: str, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if not text.strip():
        return []

    raw_chunks: list[str] = []
    current = ""
    for paragraph in split_paragraphs(text):
        for piece in split_long_text(paragraph, max_chars):
            candidate = piece if not current else current + "\n\n" + piece
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    raw_chunks.append(current)
                current = piece
    if current:
        raw_chunks.append(current)

    return apply_overlap(raw_chunks, overlap=overlap, max_chars=max_chars)


def chunk_document(doc: dict, max_chars: int = CHUNK_MAX_CHARS, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    chunks = []
    for index, text in enumerate(chunk_text(doc["text"], max_chars=max_chars, overlap=overlap)):
        chunks.append(
            {
                "chunk_id": f"{doc['doc_id']}::{index}",
                "doc_id": doc["doc_id"],
                "name": doc["name"],
                "source_file": doc.get("source_file", ""),
                "text": text,
            }
        )
    return chunks


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def run(input_path: Path = DOCUMENTS_JSONL, output_path: Path = CHUNKS_JSONL) -> int:
    if not input_path.exists():
        raise FileNotFoundError(f"Documents file not found: {input_path}")
    documents = load_jsonl(input_path)
    chunks: list[dict] = []
    for doc in documents:
        chunks.extend(chunk_document(doc))
    write_jsonl(chunks, output_path)
    return len(chunks)


def main() -> None:
    count = run()
    print(f"Written {count} chunks -> {CHUNKS_JSONL}")


if __name__ == "__main__":
    main()
