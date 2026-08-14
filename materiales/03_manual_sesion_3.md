# Sesión 3 · De agente a aplicación

Guía del estudiante para persistencia, API, interfaz y nube.


> **SDK verificado (agosto de 2026).** Estos materiales usan `azure-ai-projects` **2.4.0**, API v1, agentes versionados, Conversations y Responses. No mezcles ejemplos 1.x/classic. Revisa la [referencia 2.4.0](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme), el [quickstart 2.x](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code) y [File Search](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/file-search).

## Resultado de aprendizaje

Podrás publicar versiones, reutilizar un agente por nombre, mantener memoria con `conversation_id`, exponer `/chat` y preparar un despliegue seguro.

## Persistencia

```python
openai = project.get_openai_client(agent_name=os.environ["AGENT_NAME"])
```
Publica una versión cuando cambie la definición; conversa muchas veces.

## Contrato de API

Entrada: `mensaje` y `conversation_id` opcional. Salida: `respuesta` y `conversation_id`. El cliente guarda el ID para continuar la conversación.

## Ejecución local

```bash
uvicorn api:app --reload --port 8000
# abre http://localhost:8000/docs
```

## Pruebas por capas

1. Backend en `/docs`.
2. Dos mensajes con el mismo `conversation_id`.
3. Interfaz web.
4. AGENT_NAME inválido y backend detenido.
5. Logs sin PII ni secretos.

## Producción

Autenticación de usuarios, CORS restringido, managed identity para Azure, rate limits, timeouts, almacenamiento seguro del hilo y observabilidad.

## Checklist

- No se recrea el agente.
- `.env` no está en Git.
- Los errores son controlados.
- La URL pública tiene protección.
- Existe una instrucción de limpieza.

