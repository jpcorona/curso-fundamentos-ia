import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
 
# crear agente: modelo + nombre + instrucciones
agent = project.agents.create_version(
    agent_name="mi-primer-agente",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=(
        "Eres un experto en futbol,"
        "de equipos de alemania."
        ),
    ),
)

print(f"Agente creado con id: {agent.id}")

# Invoca el agente mediante el cliente OpenAI compatible con Foundry.
with project.get_openai_client() as openai_client:
    response = openai_client.responses.create(
        input="Hola, en una frase: ¿que puedes hacer por mi?",
        extra_body={
            "agent_reference": {
                "name": "mi-primer-agente",
                "type": "agent_reference",
            }
        },
    )

    # Muestra la respuesta generada por el agente.
    print(response.output_text)

