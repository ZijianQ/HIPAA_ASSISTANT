import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ollama

TEXT_FILE = "data/hipaa_chunks.json"             # ← 必须修正成这个
META_FILE = "data/hipaa_metadata.json"           # ← 如果需要元数据
INDEX_FILE = "data/hipaa_faiss_index.faiss"

# Load chunks
with open(TEXT_FILE, "r", encoding="utf-8") as f:
    CHUNKS = json.load(f)

# Load FAISS
INDEX = faiss.read_index(INDEX_FILE)

# Embedding model
EMB = SentenceTransformer("BAAI/bge-base-en")


def search(query, k=5):
    """Return top-k relevant chunks."""
    q_emb = EMB.encode([query], convert_to_numpy=True).astype("float32")
    D, I = INDEX.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append({
            "text": CHUNKS[idx]["text"]
        })
    return results


def generate_answer(query, retrieved_chunks):
    """RAG answer using Ollama."""
    context = "\n\n".join([c["text"] for c in retrieved_chunks])

    prompt = f"""
You are a HIPAA compliance assistant.
Use ONLY the context to answer the question.
Do NOT hallucinate. Cite text explicitly.

Context:
{context}

Question:
{query}

Answer:
"""

    resp = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.0}
    )
    return resp["message"]["content"]
