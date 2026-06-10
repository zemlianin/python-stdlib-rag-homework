import pickle

import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer

from app.chunker import write_jsonl
from app.generator import build_answer
from app.prompts import REFUSAL_NO_CONTEXT
from app.retriever import Retriever


def make_test_index(tmp_path):
    chunks = [
        {"doc_id": "1", "name": "gzip.open", "text": "gzip opens compressed files in binary or text mode"},
        {"doc_id": "2", "name": "argparse.ArgumentParser", "text": "argparse parses command line arguments and options"},
    ]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([chunk["text"] for chunk in chunks])
    vectorizer_path = tmp_path / "vectorizer.pkl"
    matrix_path = tmp_path / "matrix.npz"
    chunks_path = tmp_path / "chunks.jsonl"
    with vectorizer_path.open("wb") as file:
        pickle.dump(vectorizer, file)
    scipy.sparse.save_npz(matrix_path, matrix)
    write_jsonl(chunks, chunks_path)
    return vectorizer_path, matrix_path, chunks_path


def test_retriever_returns_best_hit(tmp_path):
    paths = make_test_index(tmp_path)
    retriever = Retriever(*paths)
    results = retriever.search("compressed gzip", k=1)
    assert results[0]["doc_id"] == "1"
    assert results[0]["score"] > 0


def test_retriever_returns_zero_for_unseen_words(tmp_path):
    paths = make_test_index(tmp_path)
    retriever = Retriever(*paths)
    results = retriever.search("борщ картошка свекла", k=1)
    assert results[0]["score"] == 0


def test_generator_refuses_when_no_relevant_context():
    answer = build_answer([{"score": 0.0, "doc_id": "x", "name": "x", "text": "irrelevant"}])
    assert answer == REFUSAL_NO_CONTEXT
