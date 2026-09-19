import os
from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.data.regulatory_db import extract_and_store_regulatory_update_from_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def _find_pdf_url(page_html: str) -> str:
    soup = BeautifulSoup(page_html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".pdf" in href or "download" in href.lower() or "token" in href.lower():
            return href
    for link in soup.find_all(["a", "iframe"]):
        src = link.get("href") or link.get("src")
        if src and "docs.google.com/gview" in src:
            return src
    raise ValueError("No PDF link could be found on the source page")


def _extract_pdf_text(pdf_path: str) -> str:
    full_text = ""

    try:
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception:
        pass

    if not full_text.strip():
        try:
            import io

            import fitz  # PyMuPDF
            import pytesseract
            from PIL import Image

            doc = fitz.open(pdf_path)
            for idx in range(min(2, len(doc))):
                page = doc[idx]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                full_text += pytesseract.image_to_string(img, lang="ara") + "\n"
            doc.close()
        except ImportError as exc:
            raise RuntimeError(f"OCR dependencies are missing: {exc}") from exc

    if not full_text.strip():
        raise ValueError("No readable text could be extracted from the legal PDF")

    return full_text.strip()


def scrape_and_store_regulatory_update(
    target_url: str,
    title_ar: Optional[str] = None,
    title_en: Optional[str] = None,
    category: str = "الاستثمار والشركات",
    issuing_body: str = "مصدر تلقائي",
    effective_date: str = "",
    reference_law: str = "",
):
    if not target_url:
        raise ValueError("A source URL is required to scrape a legal update")

    response = requests.get(target_url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    pdf_link = _find_pdf_url(response.text)
    if pdf_link.startswith("/"):
        pdf_link = "https://manshurat.org" + pdf_link

    pdf_response = requests.get(pdf_link, headers=HEADERS, timeout=60)
    pdf_response.raise_for_status()

    file_name = "regulatory_update_temp.pdf"
    with open(file_name, "wb") as f:
        f.write(pdf_response.content)

    try:
        raw_text = _extract_pdf_text(file_name)
    finally:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except OSError:
                pass

    title_ar = title_ar or "تحديث تنظيمي تم جمعه تلقائيًا"
    title_en = title_en or title_ar

    return extract_and_store_regulatory_update_from_text(
        raw_text=raw_text,
        title_ar=title_ar,
        title_en=title_en,
        source_url=target_url,
        category=category,
        issuing_body=issuing_body,
        effective_date=effective_date,
        reference_law=reference_law,
    )


def main():
    try:
        scrape_and_store_regulatory_update(
            target_url="https://manshurat.org/node/21769",
            title_ar="قانون الاستثمار رقم 72 لسنة 2017 - نص قانوني تم تلخيصه تلقائيًا",
            title_en="Investment Law No. 72 of 2017 - auto summarized legal text",
            category="الاستثمار والشركات",
            issuing_body="منشورات قانونية",
        )
    except Exception as exc:
        print(f"[!] Failed to scrape and summarize legal update: {exc}")


if __name__ == "__main__":
    main()
