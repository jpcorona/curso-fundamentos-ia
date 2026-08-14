import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

POLITICA_PATH = Path(__file__).with_name("politica-vacaciones.txt")
AGENT_NAME = "agente-rrhh"


def main():
    credential = DefaultAzureCredential()
    project = AIProjectClient(
        endpoint=os.environ["PROJECT_ENDPOINT"],
        credential=credential,
    )
    openai = project.get_openai_client()
    conversation = None
    agent = None
    vector_store = None

    try:
        vector_store = openai.vector_stores.create(name="vs-politicas")
        with POLITICA_PATH.open("rb") as archivo:
            carga = openai.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=archivo,
            )
        if getattr(carga, "status", None) == "failed":
            raise RuntimeError("Foundry no pudo indexar el documento")

        agent = project.agents.create_version(
            agent_name=AGENT_NAME,
            definition=PromptAgentDefinition(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                instructions=(
                    "Responde únicamente con evidencia del documento. "
                    "Si la respuesta no aparece, dilo con claridad."
                ),
                tools=[FileSearchTool(vector_store_ids=[vector_store.id])],
            ),
        )
        conversation = openai.conversations.create()
        response = openai.responses.create(
            conversation=conversation.id,
            input="¿Cuántos días de vacaciones tengo si llevo 6 años?",
            extra_body={
                "agent_reference": {
                    "name": agent.name,
                    "type": "agent_reference",
                }
            },
        )
        print(response.output_text)
    finally:
        if conversation is not None:
            openai.conversations.delete(conversation_id=conversation.id)
        if agent is not None:
            project.agents.delete_version(
                agent_name=agent.name,
                agent_version=agent.version,
            )
        if vector_store is not None:
            openai.vector_stores.delete(vector_store_id=vector_store.id)
        openai.close()
        project.close()
        credential.close()


if __name__ == "__main__":
    main()
