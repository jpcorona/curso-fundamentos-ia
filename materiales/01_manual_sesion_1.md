# Sesión 1 · Tu primer agente

Guía del estudiante para construir, conversar y añadir herramientas.


> **SDK verificado (agosto de 2026).** Estos materiales usan `azure-ai-projects` **2.4.0**, API v1, agentes versionados, Conversations y Responses. No mezcles ejemplos 1.x/classic. Revisa la [referencia 2.4.0](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme), el [quickstart 2.x](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code) y [File Search](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/file-search).

## Resultado de aprendizaje

Podrás explicar modelo, agente, hilo, ejecución y herramienta; crear un agente; conversar con él; y añadir Code Interpreter o una función Python.

## Arquitectura

`Portal Foundry → modelo desplegado → SDK Python → agente → hilo + run → respuesta`

## Preparación

```bash
python3 --version
az version

python3 -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
az login
```

## Variables de entorno

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://.../api/projects/tu-proyecto
FOUNDRY_MODEL_NAME=tu-deployment
```
Nunca subas `.env`; inclúyelo en `.gitignore`.

## Agente base

```python
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()
agent = project.agents.create_version(
    agent_name="mi-primer-agente",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],
        instructions="Responde en español, de forma breve y verificable.",
    ),
)
conversation = openai.conversations.create()
response = openai.responses.create(
    conversation=conversation.id,
    input="¿Qué puedes hacer por mí?",
    extra_body={"agent_reference": {
        "name": agent.name, "type": "agent_reference"
    }},
)
print(response.output_text)
```

## Añadir herramientas

1. **Code Interpreter:** úsalo para cálculo y archivos; indica en las instrucciones cuándo debe activarse.
2. **Function tool:** crea una función tipada, documenta parámetros, valida entradas y devuelve una salida pequeña.
3. Prueba un caso feliz, uno fuera de alcance y uno que obligue a usar la herramienta.

## Diagnóstico

- 401: ejecuta `az login` y revisa tenant/rol.
- 404 deployment: copia el nombre exacto.
- Endpoint: usa el del proyecto.
- `ModuleNotFoundError`: activa `.venv`.
- 429: revisa cuota y reintenta.

## Definición de terminado

El agente responde; una prueba usa herramienta; una prueba límite no inventa; el repositorio no contiene secretos.

