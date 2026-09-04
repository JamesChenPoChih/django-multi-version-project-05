import requests
from django.conf import settings


class LocalNemotronError(RuntimeError):
    pass


def chat_with_nemotron(messages):
    url = f"{settings.RAG_LLM_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        'Authorization': f"Bearer {settings.RAG_LLM_API_KEY}",
        'Content-Type': 'application/json',
    }
    payload = {
        'model': settings.RAG_LLM_MODEL,
        'messages': messages,
        'temperature': 0.2,
        'top_p': 0.9,
        'max_tokens': 700,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=settings.RAG_LLM_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LocalNemotronError(
            'Local Nemotron server is not reachable. Start Ollama/llama.cpp/vLLM first, '
            'then try again. Default Ollama command: '
            'ollama run hf.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_M'
        ) from exc

    data = response.json()
    try:
        return data['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise LocalNemotronError('Local Nemotron server returned an unexpected response.') from exc
