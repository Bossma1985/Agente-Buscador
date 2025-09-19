import streamlit as st
from agent_utils import obtener_resultados
import os

st.set_page_config(
    page_title="😈 Soy Lucy, tu asistente virtual",
    page_icon="🧠"
)

st.markdown("<h1>😈 Soy Lucy, tu asistente virtual</h1>", unsafe_allow_html=True)
st.markdown("### 🔍 Busca información en internet o 🎨 Crea imágenes")

consulta = st.text_input("¿Qué quieres saber o crear hoy?", placeholder="Ej: 'Busca información sobre Python' o 'Crea una imagen de un gato ninja'")

if st.button("🚀 ¡Hazlo, Lucy!"):
    if consulta.strip():
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

        if not GROQ_API_KEY or not TAVILY_API_KEY:
            st.error("❌ Faltan claves API en las variables de entorno")
        else:
            # Detectar si es una solicitud de imagen
            palabras_imagen = ["crea", "genera", "dibuja", "imagen", "foto", "picture", "draw", "create", "generate"]
            es_imagen = any(palabra in consulta.lower() for palabra in palabras_imagen)
            
            if es_imagen:
                with st.spinner("🎨 Lucy está creando tu imagen..."):
                    respuesta = obtener_resultados(consulta)
                st.success("✅ ¡Lucy ha terminado!")
                st.write(respuesta)
                
                # Buscar imagen generada y mostrarla
                import glob
                imagenes = glob.glob("generated_image_*.png")
                if imagenes:
                    # Mostrar la imagen más reciente
                    imagen_reciente = max(imagenes, key=os.path.getctime)
                    st.image(imagen_reciente, caption="🎨 Imagen creada por Lucy", use_column_width=True)
            else:
                with st.spinner("🕵️ Lucy está investigando..."):
                    respuesta = obtener_resultados(consulta)
                st.success("✅ ¡Esto es lo que Lucy encontró!")
                st.write(respuesta)
