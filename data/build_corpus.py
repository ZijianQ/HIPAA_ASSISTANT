import os

CLEAN_DIR = "clean"
OUT_DIR = "corpus"
os.makedirs(OUT_DIR, exist_ok=True)

FILES = [
    "hipaa_part160.txt",
    "hipaa_part164.txt",
    "de_identification.txt",
    "minimum_necessary.txt"
]

OUTPUT_FILE = os.path.join(OUT_DIR, "hipaa_corpus.txt")


def clean_text(text):
    """Basic cleanup: remove repeated blank lines, trim spaces."""
    lines = [line.strip() for line in text.splitlines()]
    # remove empty consecutive lines
    cleaned = []
    for line in lines:
        if line or (cleaned and cleaned[-1]):
            cleaned.append(line)
    return "\n".join(cleaned)


def load_and_tag(filename):
    """Add source header so later RAG can attribute citations."""
    path = os.path.join(CLEAN_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    source_title = filename.replace(".txt", "").replace("_", " ").upper()
    header = f"\n============================\nSOURCE: {source_title}\n============================\n\n"

    return header + clean_text(text) + "\n\n"


if __name__ == "__main__":
    print("\n🚀 Building unified HIPAA corpus...\n")

    corpus = ""

    for file in FILES:
        print(f"📄 Adding: {file}")
        corpus += load_and_tag(file)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(corpus)

    print(f"\n🎉 Corpus built successfully: {OUTPUT_FILE}")
    print(f"📦 Size: {len(corpus)/1024:.1f} KB")
    