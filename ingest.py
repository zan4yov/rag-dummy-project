import os
import glob
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from rag.utils import chunk_text, ensure_store

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def build(data_dir="data", store_dir="store", chunk_size=500, chunk_overlap=80):
    ensure_store(store_dir)
    model = SentenceTransformer(EMB_MODEL)

    files = sorted(list(glob.glob(os.path.join(data_dir, "*.md"))) + list(glob.glob(os.path.join(data_dir, "*.txt"))))
    if not files:
        raise FileNotFoundError(f"Tidak ada file .md / .txt di {data_dir}")

    # Prepare chunks & metadata
    chunks = []
    metas = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        for ch in chunk_text(text, chunk_size=chunk_size, overlap=chunk_overlap):
            metas.append({"path": os.path.relpath(path), "text": ch})
            chunks.append(ch)

    # Embed
    X = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
    dim = X.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(X)

    # Persist
    faiss.write_index(index, os.path.join(store_dir, "index.faiss"))
    with open(os.path.join(store_dir, "meta.jsonl"), "w", encoding="utf-8") as w:
        for m in metas:
            w.write(json.dumps(m, ensure_ascii=False) + "\n")

    with open(os.path.join(store_dir, "embeddings_model.txt"), "w", encoding="utf-8") as w:
        w.write(EMB_MODEL)

    return len(chunks)

if __name__ == "__main__":
    n = build()
    print(f"Index built with {n} chunks.")
