import requests
from bs4 import BeautifulSoup
import re

target_url = "https://manshurat.org/node/21769"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("[*] جاري الاتصال بالصفحة واستخراج رابط الـ PDF الديناميكي...")

try:
    response = requests.get(target_url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_link = None
    for a in soup.find_all('a', href=True):
        if '.pdf' in a['href'] or 'download' in a['href'] or 'token' in a['href']:
            pdf_link = a['href']
            break

    if not pdf_link:
        for link in soup.find_all(['a', 'iframe']):
            src = link.get('href') or link.get('src')
            if src and 'docs.google.com/gview' in src:
                pdf_link = src
                break

    if not pdf_link:
        print("[!] لم يتم العثور على رابط PDF صالح في الصفحة.")
        raise SystemExit(1)

    if pdf_link.startswith('/'):
        pdf_link = "https://manshurat.org" + pdf_link

    print(f"[+] تم العثور على الرابط: {pdf_link}")

    print("[*] جاري تحميل ملف الـ PDF...")
    pdf_response = requests.get(pdf_link, headers=headers, timeout=60)
    pdf_response.raise_for_status()

    file_name = "investment_law_72_2017.pdf"
    with open(file_name, 'wb') as f:
        f.write(pdf_response.content)
    print(f"[✓] تم حفظ الملف الخام باسم: {file_name}")

    full_text = ""

    # المحاولة الأولى: استخراج مباشر (لو الملف نصي)
    try:
        import pdfplumber
        with pdfplumber.open(file_name) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
    except Exception as e:
        print(f"[!] فشل الاستخراج المباشر: {e}")

    # لو الاستخراج المباشر رجع فاضي، جرب OCR
    if not full_text.strip():
        print("[*] النص فاضي - جاري تجربة OCR (الملف على الأرجح سكان)...")
        try:
            import fitz  # PyMuPDF
            import pytesseract
            from PIL import Image
            import io

            doc = fitz.open(file_name)
            print(f"[*] عدد صفحات الملف: {len(doc)}")

            # للـ POC، هنجرب أول صفحتين بس (فيها مواد الإصدار غالبًا)
            for page_num in range(min(2, len(doc))):
                page = doc[page_num]
                # تكبير الصورة لدقة أعلى (zoom=2 يعادل 144 DPI تقريبًا)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))

                print(f"[*] جاري عمل OCR على صفحة {page_num + 1}...")
                page_ocr_text = pytesseract.image_to_string(img, lang='ara')
                full_text += page_ocr_text + "\n"

            doc.close()

            if full_text.strip():
                print("[✓] تم استخراج النص عبر OCR بنجاح.")
            else:
                print("[!] الـ OCR رجع نص فاضي كمان - راجع جودة الصورة يدويًا.")

        except ImportError as e:
            print(f"[!] مكتبة ناقصة للـ OCR: {e}")
            print("ثبّتها بـ: pip install pymupdf pytesseract")
    else:
        print("[✓] تم استخراج النص مباشرة (الملف نصي، من غير حاجة لـ OCR).")

    # حفظ النص الكامل في ملف للمراجعة اليدوية
    if full_text.strip():
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
        print("[✓] تم حفظ النص الكامل في extracted_text.txt للمراجعة")

        # محاولة عزل "المادة 1 إصدار"
        match = re.search(r"المادة\s*1\s*إصدار.*?(?=المادة\s*2|\Z)", full_text, re.DOTALL)
        if match:
            article_text = match.group(0).strip()
            print("\n--- نص المادة 1 إصدار المستخرج ---")
            print(article_text)
        else:
            print("[!] لم يتم إيجاد 'المادة 1 إصدار' تلقائيًا - راجع extracted_text.txt يدويًا.")

except requests.exceptions.RequestException as e:
    print(f"[!] خطأ في الاتصال بالشبكة: {str(e)}")
except Exception as e:
    print(f"[!] حدث خطأ غير متوقع: {str(e)}")
