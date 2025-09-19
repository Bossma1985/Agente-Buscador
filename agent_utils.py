import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

# 🔑 Cargar variables desde .env
load_dotenv()

# 🔑 Leer claves API desde variables de entorno
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 🤖 Definición de nuestro agente
agente = Agent(
    "groq:llama-3.1-8b-instant",
    tools=[tavily_search_tool(TAVILY_API_KEY)],
    system_prompt="""Eres un asistente experto en búsqueda web. Tu única herramienta disponible es tavily_search_tool para buscar información en internet.

INSTRUCCIONES IMPORTANTES:
- SOLO puedes usar tavily_search_tool para buscar información
- NO inventes ni llames herramientas que no existen
- NO generes código con llamadas a funciones personalizadas
- Responde de forma clara y directa basándote en la información encontrada
- Si necesitas buscar información, usa únicamente tavily_search_tool

Responde en español de manera clara y útil."""
)

# 🔍 Función para obtener resultados
def obtener_resultados(consulta: str) -> str:
    resultado = agente.run_sync(consulta)
    return resultado.output
