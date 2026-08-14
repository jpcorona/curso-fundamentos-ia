"""
Sesión 2 · Partes 07–09 — Llamada a una API real.
Reemplaza la función falsa de la Sesión 1 por una llamada HTTP real a
Open-Meteo (gratuita, sin clave).
Ejecuta:  python agente_clima_real.py
"""
import os
import requests
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder

load_dotenv()


def obtener_clima_real(ciudad: str) -> str:
    """Consulta el clima actual real de una ciudad usando Open-Meteo.

    :param ciudad: Nombre de la ciudad (ej. "Santiago").
    :return: Descripción del clima actual, o un aviso si no se encuentra.
    """
    # 1) Ciudad -> coordenadas (API de geocoding, sin clave).
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": ciudad, "count": 1, "language": "es"},
        timeout=10,
    ).json()

    if not geo.get("results"):
        return f"No encontré la ciudad '{ciudad}'."

    lugar = geo["results"][0]

    # 2) Coordenadas -> clima actual.
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lugar["latitude"],
            "longitude": lugar["longitude"],
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    ).json()

    actual = clima["current"]
    return (
        f"En {lugar['name']}: {actual['temperature_2m']} grados C, "
        f"viento {actual['wind_speed_10m']} km/h."
    )


project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Registrar la función real como herramienta.
funciones = FunctionTool({obtener_clima_real})
toolset = ToolSet()
toolset.add(funciones)
project.agents.enable_auto_function_calls(toolset)

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="agente-clima-real",
    instructions="Eres un asistente del clima. Usa la herramienta para datos reales.",
    toolset=toolset,
)

thread = project.agents.threads.create()
project.agents.messages.create(
    thread_id=thread.id, role="user",
    content="¿Qué clima hace ahora mismo en Valparaíso?",
)
run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
if run.status == "failed":
    print(f"La ejecución falló: {run.last_error}")

for m in project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
    if m.text_messages:
        print(f"{m.role}: {m.text_messages[-1].text.value}")
