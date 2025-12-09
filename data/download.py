import os
import requests

SAVE_DIR = "raw"
os.makedirs(SAVE_DIR, exist_ok=True)

# -----------------------------
# 1) Two PDFs (De-ID & Minimum Necessary)
# -----------------------------
PDFS = {
    "de_identification": "https://www.privacysecurityacademy.com/wp-content/uploads/2021/09/HHS-OCR-Guidance-on-De-Identification-of-PHI-2012-1.pdf",
    "minimum_necessary": "https://www.sog.unc.edu/sites/default/files/additional_files/Minimum%20necessary-May%202013.pdf"
}

# -----------------------------
# 2) ECFR HTML: 45 CFR Part 160 & 164
# -----------------------------
HTML_SOURCES = {
    "hipaa_part160.html":
        "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-45?subtitle=A&subchapter=C&part=160",

    "hipaa_part164.html":
        "https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-45?subtitle=A&subchapter=C&part=164"
}


# -----------------------------
# Download PDF with simple headers
# -----------------------------
def download_pdf(name, url):
    print(f"\n⬇ Downloading PDF: {name} ...")
    try:
        r = requests.get(url, timeout=20)
        ctype = r.headers.get("Content-Type", "")

        if r.status_code == 200 and "pdf" in ctype:
            path = os.path.join(SAVE_DIR, f"{name}.pdf")
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"✅ Saved: {path} ({len(r.content)/1024:.1f} KB)")
        else:
            print(f"❌ Failed: HTTP {r.status_code}, Content-Type = {ctype}")

    except Exception as e:
        print(f"❌ Error downloading {name}: {e}")


# -----------------------------
# Download HTML from ECFR API
# -----------------------------
def download_html(name, url):
    print(f"\n⬇ Downloading ECFR HTML: {name} ...")
    try:
        r = requests.get(url, timeout=20)

        if r.status_code == 200 and "html" in r.headers.get("Content-Type", ""):
            path = os.path.join(SAVE_DIR, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"✅ Saved: {path} ({len(r.text)/1024:.1f} KB)")
        else:
            print(f"❌ Failed: HTTP {r.status_code}, Content-Type = {r.headers.get('Content-Type')}")

    except Exception as e:
        print(f"❌ Error downloading {name}: {e}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("\n🚀 Starting download of all HIPAA legal sources...\n")

    # 1) PDFs
    for filename, link in PDFS.items():
        download_pdf(filename, link)

    # 2) HTML Regulations
    for filename, link in HTML_SOURCES.items():
        download_html(filename, link)

    print("\n🎉 All HIPAA sources downloaded into /raw/ folder!\n")
