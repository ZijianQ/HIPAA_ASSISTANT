import os
import re
import json

CLEAN_DIR = "clean"
OUT_FILE = "hipaa_chunks.json"

FILES = {
    "hipaa_part160.txt": "HIPAA_PART_160",
    "hipaa_part164.txt": "HIPAA_PART_164",
    "de_identification.txt": "DE_IDENTIFICATION_GUIDANCE",
    "minimum_necessary.txt": "MINIMUM_NECESSARY_GUIDANCE",
}


def split_sentences(text):
    text = text.replace("\r", "\n")
    paras, buf = [], []
    for line in text.splitlines():
        if line.strip(): buf.append(line.strip())
        else:
            if buf:
                paras.append(" ".join(buf))
                buf = []
    if buf: paras.append(" ".join(buf))

    SENT_SPLIT_RE = re.compile(r'(?<=[。！？!?\.])\s+')
    sents = []
    for p in paras:
        parts = SENT_SPLIT_RE.split(p)
        sents += [x.strip() for x in parts if x.strip()]
    return sents


if __name__ == "__main__":
    all_chunks = []
    cid = 0

    for filename, source_name in FILES.items():
        path = os.path.join(CLEAN_DIR, filename)
        text = open(path, "r", encoding="utf-8").read()
        sentences = split_sentences(text)

        # -------- Sentence chunks --------
        for s in sentences:
            cid += 1
            all_chunks.append({
                "id": cid,
                "source": source_name,
                "type": "sentence",
                "text": s
            })

        # -------- Sliding window chunks (size=5) --------
        window = 3
        stride = 2
        for i in range(len(sentences) - window + 1):
            chunk = " ".join(sentences[i:i+window])
            cid += 1
            all_chunks.append({
                "id": cid,
                "source": source_name,
                "type": "window5",
                "text": chunk
            })

    print(f"Total chunks: {len(all_chunks)}")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print("Saved to hipaa_chunks.json")
