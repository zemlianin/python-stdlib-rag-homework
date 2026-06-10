"""Demo answer generation without external LLM."""

from __future__ import annotations

from app.config import MIN_SCORE, TOP_K
from app.prompts import REFUSAL_EMPTY_QUESTION, REFUSAL_NO_CONTEXT
from app.retriever import Retriever


def relevant_hits(hits: list[dict], min_score: float = MIN_SCORE) -> list[dict]:
    return [hit for hit in hits if hit["score"] >= min_score]


def build_answer(hits: list[dict]) -> str:
    relevant = relevant_hits(hits)
    if not relevant:
        return REFUSAL_NO_CONTEXT

    lines = ["На основании найденных фрагментов:"]
    for i, hit in enumerate(relevant, 1):
        preview = hit["text"].strip()
        lines.append(f"\n[{i}] {hit['name']}")
        lines.append(f"doc_id={hit['doc_id']}, score={hit['score']:.3f}")
        lines.append(preview)
    return "\n".join(lines)


def format_sources(hits: list[dict]) -> list[dict]:
    return [
        {
            "doc_id": hit["doc_id"],
            "name": hit.get("name", ""),
            "source_file": hit.get("source_file", ""),
            "text": hit["text"],
            "score": hit["score"],
        }
        for hit in hits
    ]


def ask(question: str, k: int = TOP_K, retriever: Retriever | None = None) -> dict:
    if not question.strip():
        return {"answer": REFUSAL_EMPTY_QUESTION, "sources": []}
    active_retriever = retriever or Retriever()
    hits = active_retriever.search(question.strip(), k=k)
    return {"answer": build_answer(hits), "sources": format_sources(hits)}
