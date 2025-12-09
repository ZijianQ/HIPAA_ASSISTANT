import json
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

CHUNK_FILE = "hipaa_chunks.json"
OUT_INDEX = "hipaa_faiss_index.faiss"
OUT_META = "hipaa_metadata.json"

model = SentenceTransformer("BAAI/bge-base-en")


def load_chunks():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, OUT_INDEX)
    print(f"✔ Saved FAISS index: {OUT_INDEX}")


if __name__ == "__main__":
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    # --- Encode all texts ---
    texts = [c["text"] for c in chunks]
    print("Embedding...")

    embeddings = model.encode(texts, batch_size=32, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    # Save index
    build_index(embeddings)

    # Save metadata (id, text, etc.)
    meta = [
        {
            "id": chunks[i]["id"],
            "text": chunks[i]["text"],
            "source": chunks[i]["source"],
            "type": chunks[i]["type"]
        }
        for i in range(len(chunks))
    ]

    with open(OUT_META, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"✔ Saved metadata: {OUT_META}")
    print("🎉 Embedding + FAISS construction complete!")
