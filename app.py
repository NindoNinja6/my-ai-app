import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- KONFIGURASI ---
API_KEY = "AIzaSyCyrI9LuPHCOrYk4iXn831Vz0wvuWNPVUo"
LINK_SHEET = "https://docs.google.com/spreadsheets/d/1e5qxD7TAR68C_dJ5A8X9k4R10-tLdqbi00SgIrmS8vY/edit?usp=sharing"
INSTRUKSI_C2N = """
("A powerful AI-driven tool for content creators to generate viral video scripts, visuals, and SEO metadata using Google Gemini.")
"""

st.set_page_config(page_title="C2N AI Video Maker", page_icon="🎬")

def check_access(email):
    try:
        url_csv = LINK_SHEET.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(url_csv)
        return email.lower().strip() in df.astype(str).apply(lambda x: x.str.lower().str.strip()).values
    except: return False

with st.sidebar:
    st.title("🎬 C2N AI Video Maker Login")
    user_email = st.text_input("Email Anda:").lower().strip()

if user_email:
    if check_access(user_email):
        try:
            genai.configure(api_key=API_KEY)
            
            # --- FITUR AUTO-DETECT MODEL ---
            if "model_name" not in st.session_state:
                # Mencari model yang tersedia untuk API Key Anda
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # Prioritas: 1.5-flash, lalu 1.5-pro, lalu gemini-pro
                if 'models/gemini-1.5-flash' in available_models:
                    st.session_state.model_name = 'gemini-1.5-flash'
                elif 'models/gemini-1.5-pro' in available_models:
                    st.session_state.model_name = 'gemini-1.5-pro'
                else:
                    st.session_state.model_name = 'gemini-pro'

            model = genai.GenerativeModel(
                model_name=st.session_state.model_name,
                system_instruction=INSTRUKSI_C2N
            )

            if "messages" not in st.session_state:
                st.session_state.messages = []

            st.title("🚀 C2N AI Video Maker")
            st.caption(f"Menggunakan Model: {st.session_state.model_name}")

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

        except Exception as e:
            st.error(f"⚠️ Terjadi Kendala: {e}")
            st.info("Coba cek apakah API Key Anda sudah benar atau buat API Key baru di Google AI Studio.")
    else:
        st.error("Akses ditolak. Email tidak terdaftar.")
else:
    st.info("Silakan login di sidebar.")
