# HackerMoose Django MCP Server

This project can run as a local MCP server so AI clients can call selected Django backend tools.

## Install

```powershell
python -m pip install -r requirements.txt
```

## Run

For most local MCP clients, configure the client to launch the server over stdio:

```powershell
python C:\Users\JamesChen\Develop_for_Web_APP\Codex\Django\login_record5_20260831_HackerMooseAI\project\rag\mcp_server.py
```

When launched manually, the process waits for MCP protocol messages on stdin. It will look quiet; that is normal.

## Client Config Example

```json
{
  "mcpServers": {
    "hackermoose-django": {
      "command": "python",
      "args": [
        "C:\\Users\\JamesChen\\Develop_for_Web_APP\\Codex\\Django\\login_record5_20260831_HackerMooseAI\\project\\rag\\mcp_server.py"
      ]
    }
  }
}
```

## Available Tools

- `server_health`: Check Django/RAG/Nemotron configuration.
- `list_products`: List products from the product catalog.
- `get_product`: Get one product by id.
- `search_knowledge`: Search the RAG retriever.
- `list_knowledge_documents`: List active knowledge documents.
- `create_knowledge_document`: Add a new knowledge document.
- `ask_rag_chatbot`: Ask the same RAG + local Nemotron pipeline used by `/chatbot/`.

## Notes

- API keys stay server-side. MCP clients call typed tools; they do not receive database credentials or provider keys.
- `ask_rag_chatbot` requires the local Nemotron/Ollama server to be running.
- Read/search tools work even if Nemotron is not running.
