import streamlit as st
import base64
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama


# ============================
#   Cache heavy resources
# ============================

@st.cache_resource
def load_embedder():
    return SentenceTransformer("BAAI/bge-base-en")

@st.cache_resource
def load_index():
    return faiss.read_index("data/hipaa_faiss_index.faiss")

@st.cache_resource
def load_chunks():
    with open("data/hipaa_chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)


EMB = load_embedder()
INDEX = load_index()
CHUNKS = load_chunks()


# ============================
#   RAG search
# ============================

def search(query, k=5):
    q_emb = EMB.encode([query], convert_to_numpy=True).astype("float32")
    D, I = INDEX.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append({"text": CHUNKS[idx]["text"]})
    return results


def generate_answer(query, retrieved_chunks):
    context = "\n\n".join([c["text"] for c in retrieved_chunks])

    prompt = f"""
You are a HIPAA compliance assistant.
Use ONLY the following context to answer the question.
Be precise. Cite text explicitly. Do NOT hallucinate.

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


# ============================
#   UI styling & background
# ============================

st.set_page_config(page_title="HIPAA Compliance Assistant")

st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #ffffff !important;
    }

    .stButton > button {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }

    .stButton > button:hover {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
    }

    .stTextInput > div > div > input {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def set_bg(image_file):
    if not os.path.exists(image_file):
        st.warning(f"Background image '{image_file}' not found.")
        return

    with open(image_file, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)


set_bg("background.png")


# ============================
#      HIPAA Assistant UI
# ============================

st.title("HIPAA Compliance Assistant")

user_prompt = st.text_input("Ask a HIPAA-related question:")


# ------- FAQ Buttons -------
st.markdown("### Or try a common question:")

faq_buttons = {
    "Minimum Necessary Rule":
        "What is the HIPAA Minimum Necessary standard and when does it NOT apply?",
    "Privacy vs Security Rule":
        "What is the difference between the HIPAA Privacy Rule and Security Rule?",
    "Breach Notification":
        "When does HIPAA require breach notification and what must be included?",
    "Patient Rights":
        "What are the key patient rights under HIPAA?",
    "Daily Awareness":
        "What daily practices help maintain HIPAA compliance?",
    "Consequences":
        "What are the penalties and consequences for HIPAA violations?"
}

cols = st.columns(3)
i = 0
selected = None
for label, question in faq_buttons.items():
    if cols[i].button(label):
        selected = question
    i = (i + 1) % 3


# ------- Determine final query -------
final_query = selected or user_prompt


# ============================
#      Run HIPAA RAG Query
# ============================

def run_rag(query):
    if not query:
        st.warning("Please enter a question.")
        return

    with st.spinner("Retrieving relevant HIPAA text..."):
        chunks = search(query, k=5)

    with st.spinner("Generating answer..."):
        answer = generate_answer(query, chunks)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("📚 View Retrieved Chunks"):
        for i, c in enumerate(chunks):
            st.markdown(f"**Chunk {i+1}:**")
            st.write(c["text"])
            if i < len(chunks) - 1:
                st.markdown("---")


if final_query:
    run_rag(final_query)


st.markdown("---")
st.caption("This tool provides information about HIPAA regulations. For legal advice, consult a qualified attorney.")