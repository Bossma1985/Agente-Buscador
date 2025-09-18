import streamlit as st
from agent_utils import obtener_resultados

st.set_page_config(
    page_title="🔎 Buscador Inteligente",
    page_icon="🧠"
)

st.markdown("<h1>🔎 Buscador Inteligente</h1>", unsafe_allow_html=True)

consulta = st.text_input("¿Qué quieres saber hoy?")

if st.button("🔎 Buscar"):
    if consulta.strip():
        with st.spinner("🕵️ Investigando..."):
            respuesta = obtener_resultados(consulta)
        st.success("✅ ¡Esto es lo que encontré!")
        st.write(respuesta)
