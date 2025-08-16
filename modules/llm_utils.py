import os
from typing import List
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEFAULT_MODEL = "llama-3.1-8b-instant"

def simple_text_clean(t: str) -> str:
    t = t.replace("\r", " ").replace("\t", " ")
    lines = [line.strip() for line in t.split("\n")]
    lines = [l for l in lines if l]
    return "\n".join(lines)

def _chat(messages, model: str = None, temperature: float = 0.2, max_tokens: int = 800):
    model = model or DEFAULT_MODEL
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content

def answer_with_context(question: str, context_blocks: List[str]) -> str:
    context = "\n\n---\n\n".join(context_blocks)
    sys_prompt = (
        "You are a clinical guideline assistant. Answer ONLY using the provided context. "
        "If the answer is not in the context, say 'Information not found in provided sources.' "
        "Cite the source names in parentheses when relevant."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer with a concise, clinically useful response."
    return _chat([{"role":"system","content":sys_prompt}, {"role":"user","content":user_prompt}], max_tokens=700)

def summarize_text_bullets(text: str) -> str:
    sys = "You are a medical summarization assistant. Produce 4-6 concise bullet points suitable for a quick clinical read."
    user = f"Summarize the following into bullet points:\n{text}"
    return _chat([{"role":"system","content":sys},{"role":"user","content":user}], max_tokens=300)
