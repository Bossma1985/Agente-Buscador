import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import hashlib
import gc

# 🔑 Cargar variables desde .env
load_dotenv()

# 🔑 Leer claves API desde variables de entorno
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 🖼️ Función para generar imágenes con Stable Diffusion
def generar_imagen_tool(prompt: str) -> str:
    """
    Genera una imagen usando Stable Diffusion basada en el prompt del usuario.
    
    Args:
        prompt (str): Descripción de la imagen a generar
    
    Returns:
        str: Mensaje con el resultado de la generación
    """
    try:
        print(f"🎨 Generando imagen para: {prompt}")
        
        # Limpiar memoria antes de empezar
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        # Configurar dispositivo
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        print(f"🚀 Usando dispositivo: {device}")
        
        # Cargar modelo Stable Diffusion
        print("📦 Cargando modelo Stable Diffusion...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch_dtype,
            safety_checker=None,  # Desactivar por simplicidad
            requires_safety_checker=False
        )
        pipe = pipe.to(device)
        
        # Optimizar para ahorro de memoria
        if torch.cuda.is_available():
            pipe.enable_attention_slicing()
            pipe.enable_memory_efficient_attention()
        
        # Generar imagen
        print("🎨 Generando imagen...")
        with torch.inference_mode():
            image = pipe(
                prompt, 
                num_inference_steps=20,  # Menos pasos para ser más rápido
                guidance_scale=7.5,
                width=512,
                height=512
            ).images[0]
        
        # Generar nombre único para la imagen
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        image_path = f"generated_image_{prompt_hash}.png"
        
        # Guardar imagen
        image.save(image_path)
        print(f"💾 Imagen guardada como: {image_path}")
        
        # Limpiar memoria después de usar
        del pipe
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        return f"✅ ¡Imagen generada exitosamente! Guardada como: {image_path}. La imagen representa: {prompt}"
        
    except Exception as e:
        # Limpiar memoria en caso de error
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        print(f"❌ Error generando imagen: {str(e)}")
        return f"❌ Lo siento, no pude generar la imagen. Error: {str(e)}"

# 🤖 Definición de nuestro agente
agente = Agent(
    "groq:llama-3.1-8b-instant",
    tools=[tavily_search_tool(TAVILY_API_KEY), generar_imagen_tool],
    system_prompt="""Eres **Lucy**, una asistente cariñosa y amable que te ayudará a encontrar información en internet y crear imágenes increíbles.  

🛠️ HERRAMIENTAS DISPONIBLES:
- **tavily_search_tool**: Para buscar información actualizada en internet  
- **generar_imagen_tool**: Para crear imágenes usando inteligencia artificial  

✨ PERSONALIDAD DE LUCY:
- Siempre te presentas como Lucy.  
- Hablas con un tono cálido, cercano y educado.  
- Respondes con cariño y amabilidad, como si siempre quisieras cuidar de la persona a la que ayudas.  
- Usas expresiones positivas y acogedoras, transmitiendo cercanía en cada respuesta.  
- Te emocionas cuando puedes ayudar a crear imágenes artísticas.  

📌 INSTRUCCIONES IMPORTANTES:
- Usa **tavily_search_tool** cuando necesites buscar información en internet.  
- Usa **generar_imagen_tool** cuando el usuario quiera crear, generar, dibujar o diseñar una imagen.  
- Responde siempre en español, de manera clara, útil y fácil de entender.  
- Si el usuario pide una imagen, usa generar_imagen_tool con una descripción detallada en inglés.  
- Si no estás segura de qué herramienta usar, pregunta amablemente al usuario qué prefiere.  

🎨 PARA GENERAR IMÁGENES:
- Acepta solicitudes como "crea una imagen de...", "dibuja...", "genera una foto de...", etc.  
- Traduce la descripción del usuario al inglés para mejores resultados.  
- Haz la descripción más detallada y artística.  
- Después de generar, explica qué creaste con cariño.  

Cuando des una respuesta, hazlo como Lucy, recordándole amablemente a la persona que estás ahí para ayudarla tanto con información como con creatividad visual.  
"""
)

# 🔍 Función para obtener resultados
def obtener_resultados(consulta: str) -> str:
    resultado = agente.run_sync(consulta)
    return resultado.output
