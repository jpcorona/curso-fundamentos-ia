# Curso · Fundamentos de agentes de IA

Material práctico para construir agentes con **Microsoft Foundry y Python** usando Azure AI Projects 2.4.

## Ruta de aprendizaje

1. [Sesión 1 · Tu primer agente](materiales/01_manual_sesion_1.md)
2. [Sesión 2 · Agente conectado](materiales/02_manual_sesion_2.md)
3. [Sesión 3 · De agente a aplicación](materiales/03_manual_sesion_3.md)
4. [Trabajo final · Construye tu agente](materiales/04_trabajo_final.md)

Cada sesión tiene una versión Markdown para GitHub y una versión PDF diseñada para lectura o impresión.

## Ejemplos del repositorio

- `agente.py`: crea una versión de un agente y obtiene una respuesta.
- `agente_docs.py`: crea un vector store, indexa la política de vacaciones y ejecuta File Search.
- `politica-vacaciones.txt`: documento de prueba para el ejercicio RAG.

Los scripts anteriores basados en Agents classic se conservan en `legacy_sdk_1x/` para referencia, pero no forman parte del recorrido recomendado.

## Preparación

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
az login
```

Completa `.env` con el endpoint del proyecto y el nombre exacto del deployment.

## SDK verificado

El curso utiliza `azure-ai-projects` 2.4.0 y la API de datos v1:

- agentes versionados con `create_version()`;
- `PromptAgentDefinition` y herramientas desde `azure.ai.projects.models`;
- conversaciones mediante `openai.conversations`;
- ejecución mediante `openai.responses`.

Consulta [la auditoría del SDK](materiales/SDK_VERIFICADO.md). No mezcles estos ejemplos con Azure AI Projects 1.x / Agents classic.

## Seguridad

- Nunca publiques `.env`, tokens o credenciales.
- Usa identidades administradas y mínimo privilegio en producción.
- No subas información personal o confidencial a los ejercicios.
- Elimina agentes, conversaciones y vector stores de prueba cuando termines.

## Trabajo final

Cada estudiante construye un agente de su elección y lo explica mediante una demostración en video de máximo tres minutos. La guía incluye tipos de agentes, entregables, rúbrica y guion cronometrado.
