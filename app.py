import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- BAGIAN YANG HARUS ANDA ISI ---
API_KEY = "AIzaSyCv1KR9ggnfPH9Ke6yQyS9VuGao9HoRnmQ"
LINK_SHEET = "https://docs.google.com/spreadsheets/d/1e5qxD7TAR68C_dJ5A8X9k4R10-tLdqbi00SgIrmS8vY/edit?usp=sharing"
# ----------------------------------

def check_access(email_user):
    try:
        # Mengubah link sheet agar bisa dibaca otomatis
        url_csv = LINK_SHEET.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(url_csv)
        # Cek apakah email ada di daftar
        return email_user.lower().strip() in df['email'].astype(str).str.lower().str.strip().values
    except:
        return False

# Tampilan Aplikasi
st.set_page_config(page_title="My Private AI", page_icon="🔒")

st.title("🤖 AI Khusus Teman")
st.write("Silakan login dengan email yang sudah saya setujui.")

# Kotak Input Email
email_input = st.text_input("Masukkan Email Anda:", placeholder="contoh@gmail.com")

if email_input:
    if check_access(email_input):
        st.success(f"Selamat datang! Akses dibuka untuk {email_input}")
        
        # Area Chat AI
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        user_msg = st.chat_input("Tanya apa saja...")
        if user_msg:
            with st.chat_message("user"):
                st.write(user_msg)
            with st.spinner("Berpikir..."):
                response = model.generate_content(user_msg)
                with st.chat_message("assistant"):
                    st.write(response.text)
    else:
        st.error("🚫 Email Anda belum terdaftar.")
        st.info("Hubungi saya (Admin) untuk minta izin akses ke aplikasi ini.")
