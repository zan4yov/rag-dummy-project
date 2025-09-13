# Mini RAG + Streamlit (Dummy Project)

Proyek RAG mini dengan UI sederhana pakai **Streamlit**. Cocok buat demo / dipush ke GitHub.
Data dummy berisi FAQ produk fiktif *Komeng Workspace*.

## Fitur
- 🔎 Retrieval via FAISS + `sentence-transformers` (`all-MiniLM-L6-v2`).
- 🧠 LLM offline default: `google/flan-t5-small` (via `transformers`).
- ☁️ (Opsional) LLM OpenAI jika `OPENAI_API_KEY` tersedia.
- 🖥️ UI sederhana ala chat + daftar sumber.
- 📦 Script `ingest.py` untuk membangun index dari folder `data/`.

## Cara jalanin (lokal)
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Bangun index dari data/ (boleh di-skip, app akan otomatis build saat pertama kali)
python ingest.py

# Jalankan UI
streamlit run app.py
```

## Struktur repo
```
mini-rag-ui/
├─ app.py                # Streamlit app
├─ ingest.py             # Build index dari folder data/
├─ rag/
│  ├─ __init__.py
│  ├─ retriever.py       # FAISS + embeddings + search
│  ├─ llm.py             # Backend LLM (transformers atau OpenAI)
│  └─ utils.py           # helper kecil
├─ data/                 # dokumen dummy (markdown)
├─ store/                # index FAISS + metadata (dibuat otomatis)
├─ tests/
│  └─ test_retriever.py  # contoh test sederhana
├─ .streamlit/
│  └─ config.toml        # tema
├─ requirements.txt
├─ .gitignore
└─ LICENSE
```

## Menambah dokumen
- Tambahkan file `.md` atau `.txt` ke folder `data/`.
- Jalankan `python ingest.py` (atau cukup restart `streamlit run app.py` — akan auto-build jika index belum ada).

## Variabel lingkungan (opsional)
- `OPENAI_API_KEY` — kalau ada, app akan menawarkan backend OpenAI (`gpt-4o-mini` secara default).
- `MODEL_NAME` — ubah model offline (mis. `google/flan-t5-base`) bila mau.

## Catatan performa
- Model offline kecil (flan-t5-small) jalan di CPU, cukup untuk demo.
- Untuk dataset besar atau latensi rendah, sebaiknya pakai layanan LLM hosted.

## Lisensi
MIT
