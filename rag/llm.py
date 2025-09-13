import os
from typing import Callable

def _offline_generator(model_name: str = None, temperature: float = 0.3) -> Callable[[str], str]:
    # Lightweight offline text2text with transformers (FLAN-T5-small)
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import torch

    name = model_name or os.getenv("MODEL_NAME", "google/flan-t5-small")
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSeq2SeqLM.from_pretrained(name)

    def generate(prompt: str) -> str:
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            out = model.generate(
                input_ids,
                max_new_tokens=256,
                temperature=max(0.1, temperature),
                do_sample=temperature > 0.0,
            )
        return tokenizer.decode(out[0], skip_special_tokens=True)
    return generate

def _openai_generator(model: str = "gpt-4o-mini", temperature: float = 0.3) -> Callable[[str], str]:
    # Uses OpenAI if OPENAI_API_KEY is set
    from openai import OpenAI
    client = OpenAI()

    def generate(prompt: str) -> str:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers concisely in Indonesian."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content
    return generate

def get_llm(backend: str = "offline", temperature: float = 0.3):
    if backend == "openai" and os.getenv("OPENAI_API_KEY"):
        return _openai_generator(temperature=temperature)
    return _offline_generator(temperature=temperature)
