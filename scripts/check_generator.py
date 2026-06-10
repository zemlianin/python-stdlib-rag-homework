from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.generator import ask


def show(label: str, question: str) -> None:
    print(f"\n--- {label}: {question} ---")
    result = ask(question)
    print(result["answer"])
    print(f"Sources: {len(result['sources'])}")
    for source in result["sources"]:
        print(f"- doc_id={source['doc_id']} score={source['score']:.4f} name={source['name']}")


if __name__ == "__main__":
    show("demo 1", "How does gzip open compressed files?")
    show("demo 2", "How does argparse parse command line arguments?")
    show("demo 3", "What does pathlib provide for filesystem paths?")
    show("negative", "Как приготовить борщ?")
