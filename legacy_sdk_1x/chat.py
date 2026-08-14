"""
Sesión 3 · Paso 04 — Un chat de verdad en la terminal.
Reutiliza el agente por su ID y mantiene un solo hilo (memoria).
Ejecuta:  python chat.py     (escribe 'salir' para terminar)
"""
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Recuperar el agente publicado (no lo creamos de nuevo).
agent = project.agents.get_agent(os.environ["AGENT_ID"])

# Un solo hilo para toda la conversación = el agente recuerda.
thread = project.agents.threads.create()

print("Chat iniciado. Escribe 'salir' para terminar.\n")

while True:
    texto = input("Tú: ")
    if texto.lower() in ("salir", "exit", "quit"):
        break

    project.agents.messages.create(thread_id=thread.id, role="user", content=texto)
    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    if run.status == "failed":
        print(f"[error] {run.last_error}\n")
        continue

    # Tomar el último mensaje del asistente.
    for m in project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING):
        if m.role == "assistant" and m.text_messages:
            print(f"Agente: {m.text_messages[-1].text.value}\n")
            break
