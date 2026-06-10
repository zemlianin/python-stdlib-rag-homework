import json

from scripts.ingest import clean_text, run


def test_clean_text_normalizes_spaces_and_newlines():
    assert clean_text("a   b\r\n\r\n\r\n c") == "a b\n\nc"


def test_ingest_writes_jsonl(tmp_path):
    raw = tmp_path / "datasets.json"
    out = tmp_path / "documents.jsonl"
    raw.write_text(json.dumps({"datasets": [{"id": 1, "name": "n", "text": "hello world"}]}), encoding="utf-8")
    assert run(raw, out) == 1
    assert out.read_text(encoding="utf-8").count("\n") == 1
