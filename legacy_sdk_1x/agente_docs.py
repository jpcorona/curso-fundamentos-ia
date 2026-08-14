"""
Sesión 2 · Partes 04–06 — Búsqueda en tus documentos (RAG / File Search).
Sube un archivo, lo indexa en un vector store y crea un agente que responde
usando ese documento.
Ejecuta:  python agente_docs.py   (corre desde esta carpeta: usa politica-vacaciones.txt)
"""
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FilePurpose, FileSearchTool, ListSortOrder

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# 1) Subir el archivo a Foundry (propósito: usarlo con agentes).
archivo = project.agents.files.upload_and_poll(
    file_path="politica-vacaciones.txt",
    purpose=FilePurpose.AGENTS,
)
print(f"Archivo subido: {archivo.id}")

# 2) Crear un vector store (el índice de búsqueda) con ese archivo.
vector_store = project.agents.vector_stores.create_and_poll(
    file_ids=[archivo.id],
    name="vs-politicas",
)
print(f"Vector store listo: {vector_store.id}")

# 3) Crear la herramienta de búsqueda apuntando al vector store.
file_search = FileSearchTool(vector_store_ids=[vector_store.id])

# 4) Crear el agente CON la herramienta de búsqueda.
agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="agente-rrhh",
    instructions=(
        "Eres un asistente de RRHH. Responde SOLO con la información "
        "de los documentos. Si no está en ellos, dilo con claridad."
    ),
    tools=file_search.definitions,
    tool_resources=file_search.resources,
)
print(f"Agente creado: {agent.id}")

# 5) Preguntar algo que solo está en el documento.
thread = project.agents.threads.create()
project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="¿Cuántos días de vacaciones tengo si llevo 6 años en la empresa?",
)
run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
if run.status == "failed":
    print(f"La ejecución falló: {run.last_error}")

for m in project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
    if m.text_messages:
        print(f"{m.role}: {m.text_messages[-1].text.value}")
