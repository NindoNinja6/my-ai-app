import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- KONEKSI BRANKAS ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    LINK_SHEET = st.secrets["LINK_SHEET"]
    INSTRUKSI_C2N = st.secrets["INSTRUKSI_C2N"]
except Exception as e:
    st.error("Brankas (Secrets) belum terisi dengan benar. Silakan cek Settings > Secrets.")
    st.stop()

st.set_page_config(page_title="C2N AI Video Maker", page_icon="🎬")

def check_access(email):
    try:
        url_csv = LINK_SHEET.replace('/edit?usp=sharing', '/export?format=csv').replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(url_csv)
        return email.lower().strip() in df.astype(str).apply(lambda x: x.str.lower().str.strip()).values
    except:
        return False

with st.sidebar:
    st.title("🎬 C2N AI VIDEO MAKER Login")
    user_email = st.text_input("Email Anda:").lower().strip()
    st.divider()
    if st.button("Reset Percakapan"):
        st.session_state.messages = []
        st.rerun()

if user_email:
    if check_access(user_email):
        try:
            genai.configure(api_key=API_KEY)
            
            # --- JURUS AUTO-FINDER MODEL ---
            if "model_name" not in st.session_state:
                # Kita cari model yang benar-benar bisa menjawab (Generate Content)
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
                
                # Urutan prioritas model tahun 2026
                prioritas = [
                    'models/gemini-1.5-flash-latest', 
                    'models/gemini-1.5-flash',
                    'models/gemini-1.5-pro',
                    'models/gemini-pro'
                ]
                
                # Pilih yang pertama kali ketemu di daftar Google
                st.session_state.model_name = next((m for m in prioritas if m in available_models), available_models[0])

            model = genai.GenerativeModel(
                model_name=st.session_state.model_name,
                system_instruction=INSTRUKSI_C2N
            )

            if "messages" not in st.session_state:
                st.session_state.messages = []

            st.title("🚀 C2N AI Video Maker")
            st.info(f"Koneksi Stabil: Menggunakan {st.session_state.model_name}")

            for m in st.session_state.messages:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

            if prompt := st.chat_input("Apa yang ingin kita buat hari ini?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("C2N sedang bekerja..."):
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"⚠️ Terjadi Kendala: {e}")
            st.info("Saran: Coba buat API Key baru di Google AI Studio dan pastikan 'Gemini API' sudah di-enable.")
    else:
        st.error("Akses ditolak. Email tidak terdaftar.")
else:
    st.info("Silakan login untuk mulai menggunakan C2N.")
