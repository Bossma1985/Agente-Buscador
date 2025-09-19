import streamlit as st
from agent_utils import obtener_resultados
import os

st.set_page_config(
    page_title="😈 Soy Lucy, tu asistente virtual",
    page_icon="🧠"
)

st.markdown("<h1>😈 Soy Lucy, tu asistente virtual</h1>", unsafe_allow_html=True)

consulta = st.text_input("¿Qué quieres saber hoy?")

if st.button("🔎 Buscar"):
    if consulta.strip():
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

        if not GROQ_API_KEY or not TAVILY_API_KEY:
            raise ValueError("Faltan claves API en las variables de entorno")

        with st.spinner("🕵️ Investigando..."):
            respuesta = obtener_resultados(consulta)
        st.success("✅ ¡Esto es lo que encontré!")
        st.write(respuesta)
