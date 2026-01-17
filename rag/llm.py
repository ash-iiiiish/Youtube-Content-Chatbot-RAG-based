import requests

OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
MODEL = "mistral:7b"

def call_llm(final_prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": final_prompt}],
        "max_tokens": 1000,
        "stream": False
    }

    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()

    return resp.json()["choices"][0]["message"]["content"]
