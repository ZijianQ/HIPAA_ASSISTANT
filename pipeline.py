# pipeline.py
import os
import subprocess
import json

print("\n==========================")
print("🚀 HIPAA RAG FULL PIPELINE")
print("==========================\n")

# Step 1: Download raw sources
print("📥 Step 1 — Downloading raw HIPAA sources...")
subprocess.run(["python3", "download.py"])

print("\n📥 Step 1b — Downloading alternative PDFs...")
subprocess.run(["python3", "download_pdf.py"])

# Step 2: Clean text
print("\n🧹 Step 2 — Cleaning text files...")
CLEAN_DIR = "data/clean"
RAW_DIR = "data/raw"
os.makedirs(CLEAN_DIR, exist_ok=True)

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".txt") or filename.endswith(".html") or filename.endswith(".pdf"):
        src = os.path.join(RAW_DIR, filename)
        dst = os.path.join(CLEAN_DIR, filename.replace(".html", ".txt").replace(".pdf", ".txt"))

        # Try to convert HTML/PDF to plain text
        print(f"   → Cleaning: {filename}")
        subprocess.run(["pandoc", src, "-t", "plain", "-o", dst])

# Step 3: Chunking
print("\n✂️ Step 3 — Chunking HIPAA text...")
subprocess.run(["python3", "chunk_hipaa.py"])

# Step 4: Build FAISS index
print("\n🔍 Step 4 — Building FAISS vector index...")
subprocess.run(["python3", "build_faiss.py"])

print("\n🎉 Pipeline complete! You can now run:")
print("   streamlit run app.py\n")