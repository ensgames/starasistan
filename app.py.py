import streamlit as st
from google import genai

# Sayfa Ayarları
st.set_page_config(
    page_title="Star Yapay Zeka Asistanı",
    page_icon="✨",
    layout="centered",
)

st.title("✨ Star Asistan")
st.write("Star, sizin için tasarlanmış akıllı yapay zeka asistanıdır.")

# Anahtarı gizli ayarlardan alıyoruz
API_KEY = st.secrets["GOOGLE_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Star'a bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Star düşünüyor..."):
            try:
                client = genai.Client(api_key=API_KEY)
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
