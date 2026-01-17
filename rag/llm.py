import requests

OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
MODEL = "richardyoung/schematron-3b:Q4_K_M"

def call_llm(final_prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": final_prompt}],
        "max_tokens": 1000,
        "stream": False
    }

    resp = requests.post(OLLAMA_URL, json=payload)
    return resp.json()["choices"][0]["message"]["content"]
