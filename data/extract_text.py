import os
import re
import json

CLEAN_DIR = "clean"
OUT_FILE = "hipaa_mixed_chunks.json"

FILES = {
    "hipaa_part160.txt": "HIPAA_PART_160",
    "hipaa_part164.txt": "HIPAA_PART_164",
    "de_identification.txt": "DE_IDENTIFICATION_GUIDANCE",
    "minimum_necessary.txt": "MINIMUM_NECESSARY_GUIDANCE",
}

TARGET_MIN = 9000


def load_paragraphs(text):
    """Split text into paragraphs separated by blank lines."""
    par = []
    buf = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            buf.append(line)
        else:
            if buf:
                par.append(" ".join(buf))
                buf = []
    if buf:
        par.append(" ".join(buf))
    return par


def split_sentences(text):
    """Rough sentence splitter."""
    SENT_SPLIT_RE = re.compile(r'(?<=[。！？!?\.])\s+')
    parts = SENT_SPLIT_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def guess_section(text):
    m = re.search(r"§\s*(\d+\.\d+)", text)
    return m.group(1) if m else None


if __name__ == "__main__":
    print("\n🚀 Building mixed-layer chunks (sentence + window + paragraph)...\n")

    all_chunks = []
    cid = 0

    for filename, source_name in FILES.items():
        print(f"📄 Processing {filename} ({source_name})")

        path = os.path.join(CLEAN_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        # ----------------------
        # 1) Paragraph Chunks
        # ----------------------
        paragraphs = load_paragraphs(text)
        print(f"  → {len(paragraphs)} paragraphs")

        for p in paragraphs:
            cid += 1
            all_chunks.append({
                "id": cid,
                "source": source_name,
                "type": "paragraph",
                "section_hint": guess_section(p),
                "text": p
            })

        # ----------------------
        # 2) Sentence Chunks
        # ----------------------
        sentences = []
        for p in paragraphs:
            sentences.extend(split_sentences(p))

        print(f"  → {len(sentences)} sentences")

        for s in sentences:
            cid += 1
            all_chunks.append({
                "id": cid,
                "source": source_name,
                "type": "sentence",
                "section_hint": guess_section(s),
                "text": s
            })

        # ----------------------
        # 3) Sliding multi-sentence windows (size=3, stride=1)
        # ----------------------
        window_size = 3
        win_chunks = []

        for i in range(len(sentences) - window_size + 1):
            win = " ".join(sentences[i:i + window_size])
            win_chunks.append(win)

        print(f"  → {len(win_chunks)} window chunks")

        for w in win_chunks:
            cid += 1
            all_chunks.append({
                "id": cid,
                "source": source_name,
                "type": "window3",
                "section_hint": guess_section(w),
                "text": w
            })

    print(f"\n🔢 Total chunks generated: {len(all_chunks)}")

    # Guarantee >= 9000
    if len(all_chunks) < TARGET_MIN:
        print(f"⚠️ Only {len(all_chunks)} chunks — need >= {TARGET_MIN}")
        print("👉 You must increase window size to 4 or add token windows.")
    else:
        print(f"🎉 Requirement satisfied: >= {TARGET_MIN}")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\n📦 Saved to {OUT_FILE}\n")
