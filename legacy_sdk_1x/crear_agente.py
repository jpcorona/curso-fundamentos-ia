"""
Sesión 3 · Paso 03 — Crear el agente definitivo UNA sola vez.
Imprime el AGENT_ID; cópialo en tu archivo .env.
Ejecuta:  python crear_agente.py     (solo una vez)
"""
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="agente-publicado",
    instructions="Eres el asistente de la empresa. Responde claro y en español.",
)

print("==============================================")
print("  Copia este ID en tu .env como AGENT_ID:")
print(f"  AGENT_ID={agent.id}")
print("==============================================")
