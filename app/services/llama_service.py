import os
import requests
from dotenv import load_dotenv
from typing import Generator

load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434") + "/api/generate"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3:3.3")


def stream_llama_response(prompt: str, model: str = MODEL_NAME) -> Generator[str, None, None]:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    try:
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = line.decode("utf-8")
                    if chunk.startswith("data: "):
                        yield chunk.removeprefix("data: ").strip()
    except requests.exceptions.RequestException as e:
        yield f"Error: {str(e)}"
