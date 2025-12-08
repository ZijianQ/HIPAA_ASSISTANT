import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ollama

TEXT_FILE = "RAG/hipaa_texts.json"
INDEX_FILE = "RAG/hipaa_faiss_index.faiss"

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    CHUNKS = json.load(f)

INDEX = faiss.read_index(INDEX_FILE)

EMB = SentenceTransformer("BAAI/bge-base-en")


def search(query, k=2):
    q_emb = EMB.encode([query])
    D, I = INDEX.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append({
            "text": CHUNKS[idx]["text"]
        })
    return results


def generate_answer(query, retrieved_chunks):
    context = ""
    for r in retrieved_chunks:
        context += r["text"] + "\n\n"

    prompt = f"""
You are a HIPAA compliance assistant.
Use ONLY the context to answer the question.
Do NOT hallucinate. Cite text explicitly.

Context:
{context}

Question:
{query}
"""

    resp = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1, "num_predict": 256}
    )

    return resp["message"]["content"]
