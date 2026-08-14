"""
Sesión 3 · Paso 06 — Envolver el agente en una API web con FastAPI.
Levanta con:  uvicorn api:app --reload --port 8000
Prueba en:    http://localhost:8000/docs
"""
import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
agent = project.agents.get_agent(os.environ["AGENT_ID"])

app = FastAPI()

# Permite que una página web local hable con esta API (ver index.html).
# En producción, restringe allow_origins a tu dominio.
app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"],
)


class Entrada(BaseModel):
    mensaje: str
    thread_id: Optional[str] = None


@app.post("/chat")
def chat(body: Entrada):
    # Reusar el hilo si viene; si no, crear uno nuevo.
    thread_id = body.thread_id or project.agents.threads.create().id

    project.agents.messages.create(thread_id=thread_id, role="user", content=body.mensaje)
    run = project.agents.runs.create_and_process(thread_id=thread_id, agent_id=agent.id)

    respuesta = "Lo siento, hubo un error."
    if run.status != "failed":
        for m in project.agents.messages.list(thread_id=thread_id, order=ListSortOrder.DESCENDING):
            if m.role == "assistant" and m.text_messages:
                respuesta = m.text_messages[-1].text.value
                break

    return {"respuesta": respuesta, "thread_id": thread_id}
