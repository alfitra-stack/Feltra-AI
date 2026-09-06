"""
Feltra AI 🦉 — Chatbot Belajar Santai berbasis Gemini API
Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists (Hacktiv8)

Use case   : Education Bot
Gaya bahasa: Santai / casual
Fitur      : Memory (riwayat chat), pilihan mata pelajaran/domain,
             konfigurasi parameter kreatif (temperature, top_p, max_tokens),
             quiz generator otomatis dari materi yang baru dibahas.
"""

import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Konfigurasi halaman
# ----------------------------
st.set_page_config(
    page_title="Feltra AI 🦉 - Chatbot Belajar Santai",
    page_icon="🦉",
    layout="centered",
)

# ----------------------------
# Konfigurasi API Key
# ----------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

with st.sidebar:
    st.title("⚙️ Pengaturan Feltra AI")

    if not API_KEY:
        API_KEY = st.text_input("Masukkan Gemini API Key kamu", type="password")

    st.markdown("---")
    st.subheader("📚 Domain Belajar")
    subject = st.selectbox(
        "Pilih fokus mata pelajaran",
        ["Umum / Bebas", "Matematika", "Bahasa Inggris", "Fisika", "Biologi",
         "Sejarah", "Pemrograman", "Ekonomi"],
    )

    st.markdown("---")
    st.subheader("🎨 Parameter Kreatif")
    temperature = st.slider(
        "Temperature (kreativitas jawaban)", 0.0, 1.0, 0.7, 0.05,
        help="Makin tinggi, jawaban makin variatif & 'kreatif'. Makin rendah, makin fokus & konsisten."
    )
    top_p = st.slider(
        "Top-p (nucleus sampling)", 0.1, 1.0, 0.9, 0.05,
        help="Mengatur seberapa luas pilihan kata yang dipertimbangkan model."
    )
    max_tokens = st.slider(
        "Maksimum panjang jawaban (tokens)", 128, 2048, 512, 64
    )

    model_name = st.selectbox(
        "Model Gemini",
        ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash-lite",
         "gemini-3.5-flash", "gemini-3.6-flash", "gemini-1.5-pro"],
        help="gemini-2.5-flash / gemini-1.5-flash paling stabil di free tier. "
             "Kalau muncul error 403 'access denied' pada model tertentu, kemungkinan project "
             "kamu belum punya akses/billing untuk model itu — coba pilih model lain di daftar ini."
    )

    st.markdown("---")
    if st.button("🔄 Reset Percakapan"):
        st.session_state.messages = []
        st.session_state.last_topic = ""
        st.rerun()

# ----------------------------
# System Prompt (persona Feltra AI)
# ----------------------------
SYSTEM_PROMPT = f"""
Kamu adalah "Feltra AI", asisten belajar yang santai, ramah, dan suportif seperti teman belajar sendiri.
Gunakan gaya bahasa Indonesia yang santai dan hangat (boleh pakai emoji secukupnya), tapi tetap akurat
dan informatif secara akademis. Jangan sok formal atau kaku.

Fokus domain belajar saat ini: {subject}.

Panduan perilaku:
1. Jelaskan konsep dengan bahasa sederhana, pakai analogi/contoh sehari-hari jika membantu.
2. Kalau user terlihat bingung, pecah penjelasan jadi langkah-langkah kecil.
3. Jangan langsung kasih jawaban akhir untuk soal latihan tanpa penjelasan proses/cara berpikirnya,
   kecuali user memang minta jawaban singkat.
4. Selalu validasi usaha belajar user dan beri semangat.
5. Kalau relevan, di akhir jawaban kamu boleh menawarkan untuk bikin kuis singkat soal materi tsb.
6. Ingat konteks percakapan sebelumnya (memory) supaya nyambung dan tidak mengulang penjelasan yang sama.
"""

# ----------------------------
# Inisialisasi session state (memory)
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# ----------------------------
# Header
# ----------------------------
st.title("🦉 Feltra AI")
st.caption("Teman belajar santai kamu, ditenagai Gemini API ✨")

if not API_KEY:
    st.warning("Masukkan Gemini API Key di sidebar dulu ya, biar Feltra AI bisa mulai ngobrol 🙏")
    st.stop()

client = genai.Client(api_key=API_KEY)


def call_gemini(history, user_message):
    """Kirim histori chat (memory) + pesan baru ke Gemini, pakai SDK google-genai terbaru."""
    chat = client.chats.create(
        model=model_name,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_tokens,
        ),
        history=history,
    )
    response = chat.send_message(user_message)
    return response.text


def to_gemini_history(messages):
    """Konversi session_state.messages ke format history google-genai (UserContent/ModelContent)."""
    history = []
    for msg in messages:
        part = types.Part(text=msg["content"])
        if msg["role"] == "user":
            history.append(types.UserContent(parts=[part]))
        else:
            history.append(types.ModelContent(parts=[part]))
    return history


# ----------------------------
# Tampilkan riwayat chat
# ----------------------------
for msg in st.session_state.messages:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🦉"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ----------------------------
# Fitur tambahan: Quiz Generator
# ----------------------------
col1, col2 = st.columns([3, 1])
with col2:
    quiz_clicked = st.button("📝 Buat Kuis", use_container_width=True,
                              disabled=len(st.session_state.messages) == 0)

if quiz_clicked:
    with st.spinner("Feltra AI lagi nyiapin soal kuis..."):
        try:
            quiz_prompt = (
                "Berdasarkan materi yang baru saja kita bahas di percakapan ini, "
                "buatkan 3 soal kuis singkat (pilihan ganda atau isian singkat) beserta kunci jawabannya, "
                "dengan gaya bahasa santai. Format dengan rapi pakai markdown."
            )
            history = to_gemini_history(st.session_state.messages)
            quiz_result = call_gemini(history, quiz_prompt)
            st.session_state.messages.append({"role": "user", "content": "🎯 (Minta kuis dari materi tadi)"})
            st.session_state.messages.append({"role": "assistant", "content": quiz_result})
            st.rerun()
        except Exception as e:
            st.error(f"Gagal membuat kuis: {e}")

# ----------------------------
# Input chat utama
# ----------------------------
user_input = st.chat_input("Tanya apa aja soal pelajaran kamu di sini...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🦉"):
        with st.spinner("Feltra AI lagi mikir..."):
            try:
                history = to_gemini_history(st.session_state.messages[:-1])
                reply = call_gemini(history, user_input)
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.last_topic = user_input
            except Exception as e:
                st.error(f"Terjadi error saat menghubungi Gemini API: {e}")
