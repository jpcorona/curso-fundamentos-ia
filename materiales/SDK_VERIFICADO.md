# SDK verificado · Microsoft Foundry

Fecha de revisión: 13 de agosto de 2026.

## Base adoptada

- `azure-ai-projects` 2.4.0, API de datos v1.
- `AIProjectClient` desde `azure.ai.projects`.
- Herramientas y definiciones desde `azure.ai.projects.models`.
- Agentes versionados con `project.agents.create_version(...)` y `PromptAgentDefinition`.
- Conversaciones con `openai.conversations.create()`.
- Ejecución con `openai.responses.create(...)`.
- Memoria multi-turno mediante `conversation_id`.

## Patrones retirados de los ejemplos

- `project.agents.create_agent(...)`.
- `project.agents.threads`, `messages` y `runs`.
- `create_and_process(...)`.
- Herramientas importadas desde `azure.ai.agents.models`.
- `AGENT_ID` como contrato principal de la aplicación.

Esos patrones pertenecen a Azure AI Projects 1.x / Agents classic y no son compatibles con 2.x.

## Verificación local

```bash
python -m pip install -r requirements-sdk-2.4.txt
python -m pip show azure-ai-projects
python -c "from azure.ai.projects import AIProjectClient; from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool, FunctionTool, CodeInterpreterTool; print('SDK 2.x OK')"
```

## Fuentes oficiales

- https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme
- https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code
- https://learn.microsoft.com/azure/foundry/agents/how-to/tools/file-search
- https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling
- https://learn.microsoft.com/azure/foundry/agents/how-to/tools/code-interpreter
