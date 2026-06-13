import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import re

# ── Config ──────────────────────────────────────────────────────────────────
BASE_URL   = "https://server8.bmd.gov.bd"
PAGE_URL   = f"{BASE_URL}/en/p/Weather-Forecast"
SAVE_DIR   = "pdfs"
LOG_FILE   = "download_log.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def find_pdf_url(html: str) -> str | None:
    """Return the first /file/.../pdf/....pdf href found in the page."""
    soup = BeautifulSoup(html, "html.parser")
    pattern = re.compile(r"^/file/\d{4}/\d{2}/\d{2}/pdf/\d+\.pdf$")
    for tag in soup.find_all("a", href=pattern):
        return BASE_URL + tag["href"]
    # fallback: regex on raw HTML
    m = re.search(r'(/file/\d{4}/\d{2}/\d{2}/pdf/\d+\.pdf)', html)
    if m:
        return BASE_URL + m.group(1)
    return None


def log(date_str: str, status: str, url: str, filepath: str) -> None:
    """Append one row to the CSV log."""
    header_needed = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a") as f:
        if header_needed:
            f.write("date,status,pdf_url,saved_path\n")
        f.write(f"{date_str},{status},{url},{filepath}\n")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    today     = datetime.utcnow()
    date_str  = today.strftime("%Y-%m-%d")
    year_mon  = today.strftime("%Y/%m")

    print(f"[{date_str}] Fetching BMD Weather Forecast page …")

    # 1. Load the forecast page
    try:
        resp = requests.get(PAGE_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"ERROR: Could not load page — {e}")
        log(date_str, "PAGE_ERROR", PAGE_URL, "")
        raise SystemExit(1)

    # 2. Find the PDF link
    pdf_url = find_pdf_url(resp.text)
    if not pdf_url:
        print("ERROR: No PDF link found on page.")
        log(date_str, "NO_PDF_FOUND", PAGE_URL, "")
        raise SystemExit(1)

    print(f"  Found PDF → {pdf_url}")

    # 3. Download the PDF
    try:
        pdf_resp = requests.get(pdf_url, headers=HEADERS, timeout=60)
        pdf_resp.raise_for_status()
    except Exception as e:
        print(f"ERROR: Could not download PDF — {e}")
        log(date_str, "DOWNLOAD_ERROR", pdf_url, "")
        raise SystemExit(1)

    # 4. Validate it's actually a PDF (must start with %PDF)
    if not pdf_resp.content.startswith(b'%PDF'):
        print(f"ERROR: Downloaded file is not a valid PDF!")
        print(f"  Content-Type: {pdf_resp.headers.get('Content-Type', 'unknown')}")
        print(f"  First bytes: {pdf_resp.content[:50]}")
        log(date_str, "INVALID_PDF", pdf_url, "")
        raise SystemExit(1)

    # 5. Save — organised as  pdfs/YYYY/MM/YYYY-MM-DD.pdf
    save_folder = os.path.join(SAVE_DIR, year_mon)
    os.makedirs(save_folder, exist_ok=True)
    filepath = os.path.join(save_folder, f"{date_str}.pdf")

    with open(filepath, "wb") as f:
        f.write(pdf_resp.content)

    size_kb = len(pdf_resp.content) // 1024
    print(f"  Saved  → {filepath}  ({size_kb} KB)")
    log(date_str, "OK", pdf_url, filepath)


if __name__ == "__main__":
    main()
