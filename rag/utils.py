import os
import textwrap
import streamlit as st

def ensure_store(store_dir="store"):
    os.makedirs(store_dir, exist_ok=True)

def chunk_text(text, chunk_size=500, overlap=80):
    text = text.strip().replace("\r\n", "\n")
    # Simple paragraph-aware chunking
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for p in paras:
        if len(current) + len(p) + 2 <= chunk_size:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current)
            # if single paragraph longer than chunk_size, split hard
            if len(p) > chunk_size:
                for i in range(0, len(p), chunk_size - overlap):
                    chunks.append(p[i:i+chunk_size])
                current = ""
            else:
                current = p
    if current:
        chunks.append(current)
    return chunks

def format_sources_panel(docs):
    with st.expander("📎 Sumber konteks", expanded=False):
        for i, d in enumerate(docs, 1):
            st.markdown(f"**[{i}]** `{d['path']}` — skor: `{d['score']:.4f}`")
            st.code(d["text"][:800] + ("..." if len(d["text"]) > 800 else ""), language="markdown")
