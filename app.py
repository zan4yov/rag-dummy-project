import os
import time
import streamlit as st

from rag.retriever import load_or_build, search as retriever_search
from rag.llm import get_llm
from rag.utils import ensure_store, format_sources_panel

st.set_page_config(page_title="Mini RAG • Komeng", page_icon="🔎", layout="wide")

st.title("🔎 Mini RAG – Demo Sederhana")
st.caption("Dummy FAQ")

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Pengaturan")
    top_k = st.slider("Top-K dokumen", 1, 10, 4)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
    backend = st.selectbox("LLM Backend", ["Offline (FLAN-T5-small)", "OpenAI (opsional)"])
    if backend == "OpenAI (opsional)":
        if not os.getenv("OPENAI_API_KEY"):
            st.info("Set `OPENAI_API_KEY` di environment untuk mengaktifkan backend OpenAI.")
    st.markdown("---")
    st.write("📚 **Dataset**: folder `data/` (markdown)")
    if st.button("Bangun ulang index"):
        with st.spinner("Membangun ulang index…"):
            import ingest
            ingest.build()
        st.success("Index dibangun ulang!")

# Load/Build index lazily
ensure_store()
retriever = load_or_build(data_dir="data", store_dir="store")

# Chat state
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {"role":"user/assistant","content":str, "sources": list}

# Display history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            format_sources_panel(msg["sources"])

# Chat input
prompt = st.chat_input("Tanya apa saja")
if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mengambil konteks & menulis jawaban…"):
            # 1) Retrieve
            docs = retriever_search(retriever, prompt, top_k=top_k)
            # 2) Compose prompt
            context_blocks = []
            for i, d in enumerate(docs, 1):
                context_blocks.append(f"[{i}] {d['path']} — score={d['score']:.4f}\n{d['text']}\n")
            context = "\n\n".join(context_blocks)
            system_instruction = (
                "Anda adalah asisten yang menjawab SINGKAT, jelas, dan berbasis konteks. "
                "Jika jawabannya tidak ada di konteks, katakan tidak yakin."
            )
            user_prompt = f"""{system_instruction}

Pertanyaan: {prompt}

Konteks:
{context}

Jawaban:"""

            # 3) Generate
            llm = get_llm(backend=("openai" if backend.startswith("OpenAI") else "offline"), temperature=temperature)
            answer = llm(user_prompt)

            # 4) Show
            st.markdown(answer)
            format_sources_panel(docs)

            st.session_state.history.append({
                "role": "assistant",
                "content": answer,
                "sources": docs
            })
