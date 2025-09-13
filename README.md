# Mini RAG + Streamlit (Dummy Project)

Proyek RAG mini dengan UI sederhana pakai **Streamlit**. Cocok buat demo / dipush ke GitHub.
Data dummy berisi FAQ produk fiktif *Komeng Workspace*.

## Fitur
- 🔎 Retrieval via FAISS + `sentence-transformers` (`all-MiniLM-L6-v2`).
- 🧠 LLM offline default: `google/flan-t5-small` (via `transformers`).
- ☁️ (Opsional) LLM OpenAI jika `OPENAI_API_KEY` tersedia.
- 🖥️ UI sederhana ala chat + daftar sumber.
- 📦 Script `ingest.py` untuk membangun index dari folder `data/`.

Cocok untuk sektor apa?

##RAG bersifat lintas-domain. Contoh sektor & use case:

Sektor	Use Case	Dampak
| Sektor           | Use Case                                           | Dampak                                                     |
|------------------|----------------------------------------------------|------------------------------------------------------------|
| Customer Support | FAQ, troubleshooting, kebijakan pengembalian       | Jawaban konsisten & cepat, beban tiket berkurang           |
| Sales/CS         | Q&A tentang produk, harga, perbandingan            | Respons cepat, bantu discovery & objection handling        |
| HR               | Kebijakan cuti, benefit, SOP onboarding            | Kurangi pertanyaan berulang, self-service karyawan         |
| IT/Helpdesk      | Runbook, how-to tools, incident tips               | MTTR turun, dokumentasi hidup                              |
| Legal/Compliance | Kebijakan, ketentuan, ringkasan klausul            | Akses cepat ke referensi resmi                             |
| Edu/Training     | Materi pelatihan, modul belajar internal           | Pembelajaran kontekstual dari materi internal              |

Catatan: proyek ini adalah dummy; ganti dataset data/ dengan dokumen organisasi Anda agar relevan.

## Cara jalanin (lokal)
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Bangun index dari data/ (boleh di-skip, app akan otomatis build saat pertama kali)
python ingest.py

# Jalankan UI
streamlit run app.py
```

## Cara memakai fitur (end-user)

1. Masukkan pertanyaan di input chat.
2. Atur Top-K (berapa banyak potongan konteks yang dipakai; default 4). Nilai lebih tinggi = lebih luas, tapi bisa lebih "bising".
3. Atur Temperature (0.0–1.5). Lebih rendah = jawaban lebih deterministik.
4. Pilih Backend: Offline (cepat, tanpa API) atau OpenAI (jika tersedia untuk kualitas lebih baik).
5. Lihat panel Sumber untuk verifikasi fakta.
6. Klik “Bangun ulang index” di sidebar jika mengganti isi data/.

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

## FAQ singkat

Q: Perlu GPU?
A: Tidak. Proyek demo jalan di CPU. GPU mempercepat, tapi tak wajib.

Q: Kenapa jawaban kadang generik?
A: Perbesar kualitas data; kurangi Temperature; tambah Top-K secukupnya; pertimbangkan model yang lebih kuat.

Q: Bisakah membatasi agar hanya menjawab dari konteks?
A: Ya—logika prompt sudah mengarahkan. Bisa diperketat (mis. tolak jika konteks kosong).

## Lisensi
MIT
