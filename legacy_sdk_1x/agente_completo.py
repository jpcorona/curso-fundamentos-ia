"""
Sesión 2 · Parte 10 — Un agente con LAS DOS herramientas.
Combina File Search (documentos) + una función que llama a una API real,
en el mismo ToolSet. El agente elige solo qué herramienta usar.
Ejecuta:  python agente_completo.py   (desde esta carpeta: usa politica-vacaciones.txt)
"""
import os
import requests
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    FilePurpose, FileSearchTool, FunctionTool, ToolSet, ListSortOrder,
)

load_dotenv()


def obtener_clima_real(ciudad: str) -> str:
    """Consulta el clima actual real de una ciudad usando Open-Meteo.

    :param ciudad: Nombre de la ciudad (ej. "Santiago").
    """
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1, "language": "es"},
        timeout=10,
    ).json()
    if not geo.get("results"):
        return f"No encontré la ciudad '{ciudad}'."
    lugar = geo["results"][0]
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lugar["latitude"],
            "longitude": lugar["longitude"],
            "current": "temperature_2m",
        },
        timeout=10,
    ).json()
    return f"En {lugar['name']}: {clima['current']['temperature_2m']} grados C."


project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Subir el documento e indexarlo (igual que en agente_docs.py).
archivo = project.agents.files.upload_and_poll(
    file_path="politica-vacaciones.txt", purpose=FilePurpose.AGENTS,
)
vector_store = project.agents.vector_stores.create_and_poll(
    file_ids=[archivo.id], name="vs-politicas",
)

# Herramienta 1: buscar en documentos.  Herramienta 2: llamar a la API real.
file_search = FileSearchTool(vector_store_ids=[vector_store.id])
funciones = FunctionTool({obtener_clima_real})

# Meter AMBAS en el mismo toolset.
toolset = ToolSet()
toolset.add(file_search)
toolset.add(funciones)
project.agents.enable_auto_function_calls(toolset)

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="agente-todoterreno",
    instructions=(
        "Eres un asistente de la empresa. Para dudas de políticas usa los "
        "documentos; para el clima usa la herramienta. No inventes datos."
    ),
    toolset=toolset,
)

thread = project.agents.threads.create()
project.agents.messages.create(
    thread_id=thread.id, role="user",
    content="¿Cuántos días de vacaciones tengo con 6 años? ¿Y qué clima hace en Santiago?",
)
run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
if run.status == "failed":
    print(f"La ejecución falló: {run.last_error}")

for m in project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
    if m.text_messages:
        print(f"{m.role}: {m.text_messages[-1].text.value}")
