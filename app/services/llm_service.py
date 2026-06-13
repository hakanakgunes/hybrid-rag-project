import json
import requests
from transformers import pipeline
import asyncio

generator = pipeline('text-generation', model='distilgpt2')

async def generate_async(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: generator(prompt, max_new_tokens=10))
    return result[0]['generated_text']



def generate_text(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    
    return response.json()["response"]


def stream_generate_text(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            yield data.get("response", "")

            if data.get("done"):
                break

    