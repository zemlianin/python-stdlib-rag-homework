"""Streamlit UI for the educational RAG."""

from __future__ import annotations
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from app.config import INDEX_CHUNKS_JSONL, MATRIX_NPZ, MIN_SCORE, TOP_K, VECTORIZER_PKL
from app.generator import ask
from app.retriever import Retriever

DEMO_QUESTIONS = [
    "How does gzip open compressed files?",
    "How does argparse parse command line arguments?",
    "What does pathlib provide for filesystem paths?",
    "Как приготовить борщ?",
]


def index_exists() -> bool:
    return all(path.exists() for path in (VECTORIZER_PKL, MATRIX_NPZ, INDEX_CHUNKS_JSONL))


@st.cache_resource
def load_retriever() -> Retriever:
    return Retriever()


def render_chunk(i: int, source: dict, expanded: bool = True) -> None:
    label = f"[{i}] doc_id={source['doc_id']} · score={source['score']:.4f}"
    with st.expander(label, expanded=expanded):
        st.markdown(f"**{source['name']}**")
        if source.get("source_file"):
            st.caption(source["source_file"])
        st.text(source["text"])


def main() -> None:
    st.set_page_config(page_title="Python Stdlib RAG", layout="wide")
    st.title("Python Stdlib RAG")
    st.caption("Учебный RAG: Python stdlib docstrings → TF-IDF → ответ с источниками")

    if not index_exists():
        st.error("Индекс не собран. Сначала выполните: `uv run python scripts/build_index.py`")
        st.stop()

    st.sidebar.header("Demo-вопросы")
    for question in DEMO_QUESTIONS:
        if st.sidebar.button(question, use_container_width=True):
            st.session_state["question"] = question

    question = st.text_input("Ваш вопрос", key="question")
    if st.button("Спросить", type="primary"):
        if not question.strip():
            st.warning("Введите вопрос.")
            st.stop()
        result = ask(question, k=TOP_K, retriever=load_retriever())

        st.subheader("Ответ")
        st.text(result["answer"])

        st.subheader("Найденные фрагменты")
        for i, source in enumerate(result["sources"], 1):
            render_chunk(i, source, expanded=source["score"] >= MIN_SCORE)

        st.subheader("Источники")
        for i, source in enumerate(result["sources"], 1):
            render_chunk(i, source, expanded=False)


if __name__ == "__main__":
    main()
