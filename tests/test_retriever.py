import os
from rag.retriever import load_or_build, search

def test_basic_search():
    retriever = load_or_build(data_dir="data", store_dir="store")
    results = search(retriever, "berapa harga pro", top_k=5)
    assert any("Rp59.000" in r["text"] for r in results), "Pricing chunk should appear in top results"
