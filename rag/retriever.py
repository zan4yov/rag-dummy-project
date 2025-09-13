import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from .utils import ensure_store

def load_or_build(data_dir="data", store_dir="store"):
    ensure_store(store_dir)
    index_path = os.path.join(store_dir, "index.faiss")
    meta_path = os.path.join(store_dir, "meta.jsonl")
    emb_model_path = os.path.join(store_dir, "embeddings_model.txt")

    if not (os.path.exists(index_path) and os.path.exists(meta_path) and os.path.exists(emb_model_path)):
        # lazy build
        import ingest
        ingest.build(data_dir=data_dir, store_dir=store_dir)

    index = faiss.read_index(index_path)
    metas = []
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            metas.append(json.loads(line))
    with open(emb_model_path, "r", encoding="utf-8") as f:
        emb_model_name = f.read().strip()

    emb_model = SentenceTransformer(emb_model_name)
    return {"index": index, "metas": metas, "emb_model": emb_model}

def search(retriever, query, top_k=4):
    emb = retriever["emb_model"].encode([query], convert_to_numpy=True, normalize_embeddings=True)
    D, I = retriever["index"].search(emb, top_k)
    results = []
    for score, idx in zip(D[0].tolist(), I[0].tolist()):
        if idx == -1:
            continue
        m = retriever["metas"][idx]
        results.append({"text": m["text"], "path": m["path"], "score": float(score)})
    return results
