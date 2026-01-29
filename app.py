import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- ISI DATA ANDA DI SINI ---
API_KEY = "AIzaSyCv1KR9ggnfPH9Ke6yQyS9VuGao9HoRnmQ"
LINK_SHEET = "https://docs.google.com/spreadsheets/d/1e5qxD7TAR68C_dJ5A8X9k4R10-tLdqbi00SgIrmS8vY/edit?usp=sharing"

# Tempelkan teks panjang dari metadata.json tadi di sini:
INSTRUKSI_C2N = """
("description": "A powerful AI-driven tool for content creators to generate viral video scripts, visuals, and SEO metadata using Google Gemini.")
"""
# -----------------------------

def check_access(email):
    try:
        url_csv = LINK_SHEET.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(url_csv)
        return email.lower().strip() in df.astype(str).apply(lambda x: x.str.lower().str.strip()).values
    except: return False

st.set_page_config(page_title="C2N AI Video Maker", page_icon="🎬", layout="wide")

with st.sidebar:
    st.title("🎬 C2N Login")
    user_email = st.text_input("Masukkan Email Terdaftar:")
    st.divider()

if user_email:
    if check_access(user_email):
        # Memasang "Otak" C2N ke Model
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro',
            system_instruction=INSTRUKSI_C2N
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.title("🚀 C2N AI Video Maker")
        
        # Tampilkan Chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if prompt := st.chat_input("Apa yang ingin kita buat hari ini?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("C2N sedang bekerja..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    else:
        st.error("Akses ditolak. Email tidak terdaftar.")
else:
    st.info("Silakan masukkan email di sidebar untuk mulai menggunakan C2N.")
