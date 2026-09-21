import os
import tempfile
from typing import Optional
from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup

from app.data.regulatory_db import extract_and_store_regulatory_update_from_text

# Some Egyptian government sites expose outdated or incomplete certificates.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
}


def _extract_page_content(soup: BeautifulSoup) -> str:
    """Extract readable article text when no usable PDF is available."""
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    main_content = soup.find("main") or soup.find("article")
    if main_content is None:
        main_content = soup.find(
            "div",
            class_=lambda value: value and any(
                name in (value if isinstance(value, list) else value.split())
                for name in ("content", "post-content", "article-body")
            ),
        )

    text = (main_content or soup).get_text(separator="\n", strip=True)
    return text[:15000]


def _find_pdf_url(page_html: str, page_url: str) -> Optional[str]:
    soup = BeautifulSoup(page_html, "html.parser")
    for element in soup.find_all(["a", "iframe"]):
        candidate = element.get("href") or element.get("src")
        if candidate and (
            ".pdf" in candidate.lower()
            or "download" in candidate.lower()
            or "token" in candidate.lower()
        ):
            return urljoin(page_url, candidate)
    return None


def _extract_pdf_text(pdf_path: str) -> str:
    full_text = ""
    try:
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:10]:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception:
        pass

    # OCR is optional: deployments without Tesseract should still support HTML
    # pages and text-based PDFs instead of failing during import or scraping.
    if not full_text.strip():
        try:
            import io
            import fitz
            import pytesseract
            from PIL import Image

            doc = fitz.open(pdf_path)
            try:
                for page in doc[: min(2, len(doc))]:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    full_text += pytesseract.image_to_string(
                        Image.open(io.BytesIO(pix.tobytes("png"))), lang="ara"
                    ) + "\n"
            finally:
                doc.close()
        except (ImportError, OSError, RuntimeError):
            # OCR is a best-effort fallback. The caller can still use page text.
            pass

    return full_text.strip()


def _download_pdf_text(session: requests.Session, pdf_url: str) -> str:
    response = session.get(pdf_url, headers=HEADERS, verify=False, timeout=30)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name
    try:
        return _extract_pdf_text(temp_path)
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


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

    with requests.Session() as session:
        response = session.get(target_url, headers=HEADERS, verify=False, timeout=30)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").lower()
        raw_text = ""
        page_title = None
        soup = None

        if "application/pdf" in content_type or target_url.lower().split("?", 1)[0].endswith(".pdf"):
            raw_text = _download_pdf_text(session, response.url)
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            page_title = soup.title.get_text(strip=True) if soup.title else None
            pdf_link = _find_pdf_url(response.text, response.url)
            if pdf_link:
                try:
                    raw_text = _download_pdf_text(session, pdf_link)
                except requests.RequestException:
                    raw_text = ""

            # Normal article pages, and scanned/unreadable PDFs, fall back to HTML.
            if not raw_text:
                raw_text = _extract_page_content(soup)

    if not raw_text:
        raise ValueError("لم نتمكن من استخراج أي نص قانوني مقروء من الرابط المدخل.")

    return extract_and_store_regulatory_update_from_text(
        raw_text=raw_text,
        title_ar=title_ar or page_title or "تحديث تنظيمي جديد",
        title_en=title_en or "Regulatory update",
        source_url=target_url,
        category=category,
        issuing_body=issuing_body,
        effective_date=effective_date,
        reference_law=reference_law,
    )
