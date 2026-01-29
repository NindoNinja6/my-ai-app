import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- AMBIL DATA DARI SECRETS ---
API_KEY = st.secrets["GOOGLE_API_KEY"]
LINK_SHEET = st.secrets["LINK_SHEET"]
INSTRUKSI_C2N = st.secrets["INSTRUKSI_C2N"]

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

if user_email:
    if check_access(user_email):
        try:
            genai.configure(api_key=API_KEY)

            # --- LOGIKA DETEKTIF MODEL ---
            if "model_pilihan" not in st.session_state:
                # Mencari model apa saja yang bisa dipakai oleh API Key Anda
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # Prioritas: 1.5-flash, lalu 1.5-pro, lalu gemini-pro (versi lama)
                if 'models/gemini-1.5-flash' in models:
                    st.session_state.model_pilihan = 'gemini-1.5-flash'
                elif 'models/gemini-1.5-pro' in models:
                    st.session_state.model_pilihan = 'gemini-1.5-pro'
                else:
                    st.session_state.model_pilihan = 'gemini-pro'

            model = genai.GenerativeModel(
                model_name=st.session_state.model_pilihan,
                system_instruction=INSTRUKSI_C2N
            )

            if "messages" not in st.session_state:
                st.session_state.messages = []

            st.title("🚀 C2N AI Video Maker")
            st.caption(f"Status: Aktif menggunakan {st.session_state.model_pilihan}")

            for m in st.session_state.messages:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

            if prompt := st.chat_input("Apa yang ingin kita buat hari ini?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("C2N sedang memproses..."):
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"⚠️ Terjadi Kendala AI: {e}")
            st.info("Coba refresh halaman ini setelah 1 menit.")
    else:
        st.error("Akses ditolak. Email tidak terdaftar di Google Sheets.")
else:
    st.info("Silakan masukkan email di sidebar untuk mulai.")
