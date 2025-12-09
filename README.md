# HIPAA Retrieval-Augmented Generation (RAG) System

This project implements a local LLM-based RAG system with HIPAA legal documents.

## Features

- Local LLM (Qwen2.5:1.5b) via Ollama
- Vector search with FAISS
- Embedding model BGE-base-en
- Streamlit frontend for querying HIPAA
- Database contains >10,000 lines of legal text

## config

- Docker
- Python 3.9+
- Ollama

## Features

- Chatbot powered by Ollama
- Streamlit web interface

# Project Structure

```
medical-coding/
├── app.py                     # Streamlit UI
├── rag_engine.py              # RAG search + answer generator
├── pipeline.py                # One-click full pipeline
├── download.py                # ECFR HTML downloader
├── download_pdf.py            # Alternative PDF downloader
├── chunk_hipaa.py             # Chunk builder (sentence + window)
├── build_faiss.py             # Embedding + FAISS index builder
├── data/
│   ├── raw/                   # Original HTML/PDF
│   ├── clean/                 # Plain text extracted
│   ├── hipaa_chunks.json      # Final chunk dataset
│   └── hipaa_faiss_index.faiss
├── background.png             # UI background image
├── requirements.txt
└── Dockerfile
```

## Installation

### 1. Install Ollama

https://ollama.com

### 2. Pull the model

ollama pull qwen2.5:1.5b

### 3. Create virtual environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 4. running the pipelind

python3 pipeline.py

### 4. Run Streamlit app

python -m streamlit run app.py

### 5. Access the app

Open browser:
http://localhost:8501

---

## System Architecture

User → Streamlit UI  
→ Query → FAISS Index  
→ Retrieve Top-k chunks  
→ RAG prompt to Qwen2.5 model  
→ Return grounded HIPAA-compliant answer

---

## Docker Quick start

docker build -t hipaa-rag .
docker run -p 8501:8501 hipaa-rag
acess at http://localhost:8501

## Data Resource Link

45 CFR Part 160
https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-160

45 CFR Part 164（Security & Privacy）
https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164

De-identification guidance:
https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html

Minimum Necessary Guidance:
https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html
