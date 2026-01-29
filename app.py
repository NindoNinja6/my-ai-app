import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- ISI ULANG DI SINI ---
API_KEY = "AIzaSyCv1KR9ggnfPH9Ke6yQyS9VuGao9HoRnmQ"
LINK_SHEET = "https://docs.google.com/spreadsheets/d/1e5qxD7TAR68C_dJ5A8X9k4R10-tLdqbi00SgIrmS8vY/edit?usp=sharing"
# -------------------------

def check_access(email_user):
    try:
        url_csv = LINK_SHEET.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(url_csv)
        email_user_clean = email_user.lower().strip()
        return df.astype(str).apply(lambda x: x.str.lower().str.strip()).isin([email_user_clean]).any().any()
    except:
        return False

st.set_page_config(page_title="AI VIDEO MAKER", page_icon="🤖", layout="wide")

with st.sidebar:
    st.title("🔐 Akses Masuk")
    user_email = st.text_input("Masukkan Email Terdaftar:", placeholder="email@gmail.com")
    st.divider()

if user_email:
    if check_access(user_email):
        st.title("💬 Chat dengan AI Saya")
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Apa yang ingin kamu tanyakan?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Sedang mengetik..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    else:
        st.error("🚫 Email tidak terdaftar.")
else:
    st.header("👋 Selamat Datang!")
    st.write("Silakan masukkan email Anda di bagian samping (sidebar) untuk mulai.")
