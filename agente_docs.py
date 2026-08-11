import os
from pathlib import Path

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential


load_dotenv()

POLITICA_PATH = Path(__file__).with_name("politica-vacaciones.txt")
AGENT_NAME = "agente-rrhh"


def main():
    endpoint = os.environ["PROJECT_ENDPOINT"]
    modelo = os.environ["MODEL_DEPLOYMENT_NAME"]

    credential = DefaultAzureCredential()
    project = AIProjectClient(
        endpoint=endpoint,
        credential=credential,
    )
    openai = project.get_openai_client()

    conversation = None
    agent = None

    try:
        vector_store = openai.vector_stores.create(
            name="vs-politicas"
        )

        with POLITICA_PATH.open("rb") as archivo:
            carga = openai.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=archivo,
            )

        if getattr(carga, "status", None) == "failed":
            raise RuntimeError(
                "Foundry no pudo indexar politica-vacaciones.txt"
            )

        print(f"Vector store listo: {vector_store.id}")

        agent = project.agents.create_version(
            agent_name=AGENT_NAME,
            definition=PromptAgentDefinition(
                model=modelo,
                instructions=(
                    "Eres un asistente de RRHH. Responde solo con la "
                    "información de los documentos disponibles mediante "
                    "File Search. Si la respuesta no aparece en ellos, "
                    "dilo con claridad."
                ),
                tools=[
                    FileSearchTool(
                        vector_store_ids=[vector_store.id]
                    )
                ],
            ),
            description=(
                "Ejemplo docente RAG con File Search en Microsoft Foundry."
            ),
        )

        print(f"Agente creado: {agent.name} v{agent.version}")

        conversation = openai.conversations.create()

        response = openai.responses.create(
            conversation=conversation.id,
            input=(
                "¿Cuántos días de vacaciones tengo si llevo "
                "6 años en la empresa?"
            ),
            extra_body={
                "agent_reference": {
                    "name": agent.name,
                    "type": "agent_reference",
                }
            },
        )

        print("\nRespuesta del agente:")
        print(response.output_text)

    finally:
        if conversation is not None:
            try:
                openai.conversations.delete(
                    conversation_id=conversation.id
                )
            except Exception as exc:
                print(
                    f"Aviso: no se pudo borrar la conversación: {exc}"
                )

        if agent is not None:
            try:
                project.agents.delete_version(
                    agent_name=agent.name,
                    agent_version=agent.version,
                )
            except Exception as exc:
                print(
                    f"Aviso: no se pudo borrar la versión del agente: {exc}"
                )

        openai.close()
        project.close()
        credential.close()


if __name__ == "__main__":
    main()