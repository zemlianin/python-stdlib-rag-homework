from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.retriever import Retriever


def show(query: str) -> None:
    print(f"\nQuery: {query}")
    results = Retriever().search(query, k=3)
    for i, hit in enumerate(results, 1):
        preview = hit["text"][:140].replace("\n", " ")
        print(f"[{i}] doc_id={hit['doc_id']} score={hit['score']:.4f} name={hit['name']}")
        print(preview + "...")


if __name__ == "__main__":
    show("gzip compressed file")
    show("argparse command line arguments")
    show("Как приготовить борщ?")
