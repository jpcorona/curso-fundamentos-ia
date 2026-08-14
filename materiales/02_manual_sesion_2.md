# Sesión 2 · Agente conectado

Guía del estudiante para RAG, APIs reales y selección de herramientas.


> **SDK verificado (agosto de 2026).** Estos materiales usan `azure-ai-projects` **2.4.0**, API v1, agentes versionados, Conversations y Responses. No mezcles ejemplos 1.x/classic. Revisa la [referencia 2.4.0](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme), el [quickstart 2.x](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code) y [File Search](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/file-search).

## Resultado de aprendizaje

Podrás indexar documentos, consultar una API y crear un agente que elija la fuente adecuada.

## RAG en una línea

`Archivo → chunks → embeddings → vector store → recuperación → contexto → respuesta`

Indexar no es entrenar. Si la evidencia no existe, el agente debe reconocerlo.

## File Search

```python
archivo = project.agents.files.upload_and_poll(
    file_path="politica-vacaciones.txt", purpose=FilePurpose.AGENTS)
vector_store = project.agents.vector_stores.create_and_poll(
    file_ids=[archivo.id], name="vs-politicas")
file_search = FileSearchTool(vector_store_ids=[vector_store.id])
```

## API real

Usa `requests` con `timeout`, `raise_for_status()`, validación del JSON y mensajes controlados para ciudad no encontrada.

## Enrutamiento

Instrucción sugerida: “Para políticas usa los documentos; para clima usa la API; no inventes y explica límites”.

## Matriz mínima de pruebas

| Caso | Esperado |
|---|---|
| Dato en documento | Respuesta respaldada |
| Dato ausente | Declara ausencia |
| API normal | Dato actual |
| Ciudad inválida | Error controlado |
| Pregunta mixta | Usa ambas herramientas |

## Seguridad y costos

Claves en variables de entorno; archivos publicables; expiración y limpieza de vector stores; confirmación humana para acciones sensibles.

