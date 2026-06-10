"""Prepare data/raw/datasets.json from Python standard library docstrings.

The source is the local Python standard library installed with the interpreter.
Only textual module/function/class docstrings are indexed. The script is
internet-free and deterministic enough for the homework MVP.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import sysconfig
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import RAW_DATASETS  # noqa: E402

EXCLUDED_PARTS = {
    "__pycache__",
    "site-packages",
    "dist-packages",
    "ensurepip",
    "idlelib",
    "tkinter",
    "turtledemo",
    "test",
    "tests",
}


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_good_docstring(text: str) -> bool:
    cleaned = clean_text(text)
    if len(cleaned) < 80:
        return False
    alpha = sum(ch.isalpha() for ch in cleaned)
    return alpha >= 40


def iter_python_files(stdlib_root: Path) -> Iterable[Path]:
    for path in sorted(stdlib_root.rglob("*.py")):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        yield path


def extract_records_from_file(path: Path, stdlib_root: Path, start_index: int) -> list[dict]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return []

    module = path.relative_to(stdlib_root).with_suffix("").as_posix().replace("/", ".")
    records: list[dict] = []

    def add(kind: str, object_name: str, doc: str) -> None:
        if not is_good_docstring(doc):
            return
        index = start_index + len(records)
        text = (
            f"Module: {module}\n"
            f"Object: {object_name}\n"
            f"Kind: {kind}\n\n"
            f"{clean_text(doc)}"
        )
        records.append(
            {
                "id": f"py_stdlib_{index:05d}",
                "name": f"{module}.{object_name}" if object_name != module else module,
                "text": text,
                "source_file": f"stdlib/{path.relative_to(stdlib_root).as_posix()}",
                "source": "Python standard library docstrings",
                "license": "PSF License Version 2",
            }
        )

    module_doc = ast.get_docstring(tree)
    if module_doc:
        add("module", module, module_doc)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                add(type(node).__name__, node.name, doc)

    return records


def collect_records(limit: int | None = None) -> list[dict]:
    stdlib_root = Path(sysconfig.get_paths()["stdlib"]).resolve()
    records: list[dict] = []
    for path in iter_python_files(stdlib_root):
        records.extend(extract_records_from_file(path, stdlib_root, len(records)))
        if limit is not None and len(records) >= limit:
            return records[:limit]
    return records


def write_dataset(records: list[dict], output_path: Path = RAW_DATASETS) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": {
            "title": "Python standard library docstrings",
            "description": "Text records extracted from module, class and function docstrings of the locally installed Python standard library.",
            "source": "Local Python standard library source files",
            "license": "Python Software Foundation License Version 2",
            "record_count": len(records),
        },
        "datasets": records,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    records = collect_records(limit=limit)
    if len(records) < 10:
        raise RuntimeError("Too few records extracted from the standard library")
    write_dataset(records)
    print(f"Prepared {len(records)} records -> {RAW_DATASETS}")


if __name__ == "__main__":
    main()
