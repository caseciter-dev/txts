import sys
import subprocess

# --- AUTOMATIC DEPENDENCY INSTALLER ---
def install_dependencies():
    required_packages = {"requests": "requests", "pypdf": "pypdf"}
    for import_name, pip_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing missing dependency: {pip_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

install_dependencies()

import os
import requests
from pypdf import PdfReader

# The target URL you provided
PDF_URL = "https://cdn.sci-notifier.codechips.in/orders/latest.pdf"
OUTPUT_TXT_FILE = "latest_order.txt"  # Saved in the root of the repo

def main():
    local_pdf = "temp_download.pdf"
    try:
        # 1. Download the PDF
        print("Downloading PDF...")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(PDF_URL, headers=headers, stream=True)
        response.raise_for_status()
        with open(local_pdf, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # 2. Convert PDF to Plain Text
        print("Extracting text...")
        reader = PdfReader(local_pdf)
        extracted_text = ""
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text += f"--- Page {page_num + 1} ---\n{text}\n\n"
        
        # 3. Write it out to a local file inside the runner
        if extracted_text.strip():
            with open(OUTPUT_TXT_FILE, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Success! Text generated locally: {OUTPUT_TXT_FILE}")
        else:
            print("No text found in the PDF.")

    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1) # Fail the action if an error happens
    finally:
        if os.path.exists(local_pdf):
            os.remove(local_pdf)

if __name__ == "__main__":
    main()
