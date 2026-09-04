# Free Local Nemotron RAG Setup

This project calls a local OpenAI-compatible server, so there is no paid NVIDIA API usage.

## Recommended Free Model

Use NVIDIA Nemotron 3 Nano 4B GGUF:

```powershell
ollama run hf.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_M
```

The Django defaults are:

```env
RAG_LLM_BASE_URL=http://127.0.0.1:11434/v1
RAG_LLM_MODEL=hf.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_M
RAG_LLM_API_KEY=not-needed
```

## Chatbot URL

Start Django and open:

```text
http://127.0.0.1:8000/chatbot/
```

## How RAG Works

The retriever searches active `KnowledgeDocument` records, product records, and selected project files.
The answer pipeline sends the retrieved context to the local Nemotron model.

## Add Knowledge

Use Django admin to add `KnowledgeDocument` rows, or import local files:

```powershell
python manage.py ingest_knowledge README.md templates/index.html --source-prefix project:
```

Important files:

- `rag/models.py`
- `rag/admin.py`
- `rag/services/retriever.py`
- `rag/services/nemotron_client.py`
- `rag/services/rag_pipeline.py`
- `templates/rag/chatbot.html`
