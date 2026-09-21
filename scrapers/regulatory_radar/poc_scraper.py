import os
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.data.regulatory_db import extract_and_store_regulatory_update_from_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}


def _find_pdf_url(page_html: str, page_url: str) -> str:
    soup = BeautifulSoup(page_html, "html.parser")
    for element in soup.find_all(["a", "iframe"], href=True):
        candidate = element.get("href") or element.get("src")
        if candidate and (".pdf" in candidate.lower() or "download" in candidate.lower() or "token" in candidate.lower()):
            return urljoin(page_url, candidate)
    for element in soup.find_all(["a", "iframe"]):
        candidate = element.get("href") or element.get("src")
        if candidate and "docs.google.com/gview" in candidate:
            return urljoin(page_url, candidate)
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
            import fitz
            import pytesseract
            from PIL import Image
            doc = fitz.open(pdf_path)
            for idx in range(min(2, len(doc))):
                pix = doc[idx].get_pixmap(matrix=fitz.Matrix(2, 2))
                full_text += pytesseract.image_to_string(
                    Image.open(io.BytesIO(pix.tobytes("png"))), lang="ara"
                ) + "\n"
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
    content_type = response.headers.get("content-type", "").lower()
    pdf_link = target_url if "application/pdf" in content_type or target_url.lower().endswith(".pdf") else _find_pdf_url(response.text, response.url)

    pdf_response = requests.get(pdf_link, headers=HEADERS, timeout=60)
    pdf_response.raise_for_status()
    file_name = "regulatory_update_temp.pdf"
    with open(file_name, "wb") as output:
        output.write(pdf_response.content)
    try:
        raw_text = _extract_pdf_text(file_name)
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

    return extract_and_store_regulatory_update_from_text(
        raw_text=raw_text,
        title_ar=title_ar or "تحديث تنظيمي تم جمعه يدويًا",
        title_en=title_en or title_ar or "Regulatory update",
        source_url=target_url,
        category=category,
        issuing_body=issuing_body,
        effective_date=effective_date,
        reference_law=reference_law,
    )
