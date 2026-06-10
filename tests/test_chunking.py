from app.chunker import chunk_document, chunk_text, split_paragraphs


def test_split_paragraphs_ignores_empty_blocks():
    assert split_paragraphs("one\n\n\n two \n\n") == ["one", "two"]


def test_chunk_text_respects_max_chars():
    chunks = chunk_text("a" * 1200, max_chars=300, overlap=30)
    assert len(chunks) >= 4
    assert all(len(chunk) <= 300 for chunk in chunks)


def test_chunk_document_keeps_doc_metadata():
    doc = {"doc_id": "d1", "name": "demo", "source_file": "source.py", "text": "first paragraph\n\nsecond paragraph"}
    chunks = chunk_document(doc, max_chars=200, overlap=0)
    assert chunks[0]["doc_id"] == "d1"
    assert chunks[0]["name"] == "demo"
    assert chunks[0]["source_file"] == "source.py"
