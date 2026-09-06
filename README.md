# 🦉 Feltra AI — Chatbot Belajar Santai (Gemini API)

Final Project — *LLM-Based Tools and Gemini API Integration for Data Scientists* (Hacktiv8)

## 📌 Use Case
**Education Bot** — Feltra AI adalah teman belajar virtual yang membantu pengguna memahami
berbagai mata pelajaran (Matematika, Fisika, Bahasa Inggris, Pemrograman, dll.) dengan gaya
bahasa yang **santai dan suportif**, bukan seperti guru yang kaku.

## ✨ Fitur & Parameter Kreatif
| Fitur | Deskripsi |
|---|---|
| 🎨 Gaya bahasa santai | System prompt didesain agar bot menjelaskan dengan bahasa sehari-hari + emoji |
| 📚 Domain pengetahuan | User bisa memilih fokus mata pelajaran dari sidebar |
| 🧠 Memory | Riwayat percakapan disimpan dalam session sehingga bot "ingat" konteks sebelumnya |
| 📝 Quiz Generator | Fitur tambahan: membuat 3 soal kuis otomatis dari materi yang baru dibahas |
| ⚙️ Konfigurasi parameter | Slider untuk mengatur `temperature`, `top_p`, dan `max_output_tokens` secara real-time |
| 🔄 Reset percakapan | Tombol untuk memulai sesi belajar baru |

## 🛠️ Tech Stack
- **Streamlit** — antarmuka web interaktif
- **Google Gen AI SDK (`google-genai`)** — SDK resmi terbaru untuk Gemini API (menggantikan `google-generativeai` yang sudah dipensiunkan Google)
- **python-dotenv** — manajemen API key

## 🚀 Cara Menjalankan

1. **Clone repo ini**
   ```bash
   git clone <URL_REPO_KAMU>
   cd edu-buddy-chatbot
   ```

2. **Buat virtual environment (opsional tapi disarankan)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Siapkan API Key**
   - Dapatkan Gemini API key gratis di [Google AI Studio](https://aistudio.google.com/apikey)
   - Salin `.env.example` menjadi `.env`
   - Isi `GEMINI_API_KEY` dengan API key kamu

   Atau, jika tidak ingin membuat file `.env`, kamu bisa langsung memasukkan API key
   di kolom sidebar saat aplikasi berjalan.

5. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

6. Buka browser di `http://localhost:8501`

## 📸 Screenshot User Interface
> Tambahkan screenshot antarmuka aplikasi kamu di sini (misalnya di folder `screenshots/`)
>
> Contoh:
> ![Tampilan Feltra AI](screenshots/chat-view.png)

## 📂 Struktur Proyek
```
edu-buddy-chatbot/
├── app.py                # Kode utama aplikasi Streamlit
├── requirements.txt       # Daftar dependencies
├── .env.example           # Contoh konfigurasi API key
├── .gitignore
└── README.md
```

## 💡 Pengembangan Lanjutan (Ide)
- Simpan riwayat chat ke database agar persist antar sesi
- Tambah fitur upload materi (PDF) untuk dijadikan bahan tanya-jawab (RAG)
- Tambah leaderboard skor kuis
- Integrasi text-to-speech agar penjelasan bisa didengarkan
