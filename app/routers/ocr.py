from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import sqlite3
import re
from datetime import datetime
from app.database import get_db
from app.schemas import LedgerExtractionRequest, ExtractedRecord

router = APIRouter(prefix="/api/ocr", tags=["OCR & Document Parsing"])

SAMPLE_HISTORICAL_DOCS = [
    {
        "title": "مستخرج قيد ميلاد ورقي عتيق - دار المحفوظات بالقلعة (1938)",
        "sample_text": """
جمهورية مصر العربية - وزارة المالية
مصلحة دار المحفوظات العمومية - قلعة صلاح الدين بالقاهرة
مستخرج رسمي من دفتر سجل المواليد الورقي
مديرية: الدقهلية | مركز: المنصورة | ناحية / قرية: أويش الحجر
دفتر رقم: 42 صحيفة رقم: 18 لسنة: 1938 ميلادية
اسم المولود: فؤاد إبراهيم المحمودي
اسم الوالد: إبراهيم المحمودي عطية | الديانة: مسلم | الجنسية: مصري
اسم الوالدة: فاطمة حسن العدوي
تاريخ الولادة: 14 من شهر مايو سنة 1938 ميلادية
تاريخ القيد بالدفتر: 18 مايو سنة 1938
أمين الدفتر: عبد العزيز خليل | كاتب السجلات: محمد رضوان
تمت المطابقة مع الدفتر الأصلي وختم بشعار الجمهورية (نسر دار المحفوظات) بتاريخ 12 فبراير 2026.
"""
    },
    {
        "title": "صورة قيد مكلفة أطيان زراعية وعقارات قديمة (1952)",
        "sample_text": """
مصلحة الأموال المقررة والمحفوظات التاريخية
مستخرج رسمي من مكلفات الأطيان الزراعية (الدفاتر المساحية القديمة)
محافظة: الغربية | مركز: طنطا | حوض: داير الناحية نمرة 7
دفتر مكلفة رقم: 89 صفحة: 104 لسنة: 1952
اسم المكلف باسمه: الحاج عبد الرحمن توفيق الجندي
المساحة المكلفة: 4 أفدنة و 12 قيراطاً و 8 أسهم
الحدود: بحرياً مصرف نمرة 4، قبلياً ملك ورثة السعيد، شرقاً طريق زراعي، غرباً ملك الشيخ إبراهيم.
الضريبة السنوية المقررة: 14 جنيهاً مصرياً و 350 مليماً
صادر بناء على طلب المحامي الوكيل لتقديمه للجنة حصر التركات.
خاتم شعار الجمهورية وتوقيع المراجع المالي 15 يوليو 2026.
"""
    },
    {
        "title": "شهادة وفاة وقيد عائلي من سجلات الأحوال المدنية التاريخية (1964)",
        "sample_text": """
وزارة الداخلية - مصلحة الأحوال المدنية
إدارة السجلات المدنية للمناطق المحفوظة
قيد واقعة وفاة رسمية
محافظة: الإسكندرية | قسم: العطارين | شياخة: المسلة
سجل وفيات رقم: 115 صفحة رقم: 77 لسنة: 1964
اسم المتوفى: مريم يوسف جرجس
اسم الوالد: يوسف جرجس غالي | اسم الوالدة: تريزا عبد الملك
تاريخ الوفاة: 22 نوفمبر 1964 | سبب الوفاة: هبوط حاد بالدورة الدموية
المبلغ بالوفاة: نجل المتوفاة
تم القيد بسجل الوفيات الورقي بمعرفة مفتش الصحة.
صورة طبق الأصل مستخرجة ومعتمدة بخاتم شعار الدولة للأحوال المدنية بالإسكندرية.
"""
    }
]

@router.get("/samples")
def get_sample_documents():
    return SAMPLE_HISTORICAL_DOCS

@router.post("/extract", response_model=ExtractedRecord)
def extract_ledger_metadata(payload: LedgerExtractionRequest, db: sqlite3.Connection = Depends(get_db)):
    text = payload.raw_text or ""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text content is required for metadata parsing")

    # Parsing Logic using tailored regex for Egyptian administrative texts
    doc_title = payload.document_title or "مستند أرشيفي رسمي"
    
    # 1. Archive location
    archive_loc = "دار المحفوظات العمومية - القلعة"
    if "الأحوال المدنية" in text:
        archive_loc = "مصلحة الأحوال المدنية (السجلات المحفوظة)"
    elif "مكلفات" in text or "الأموال المقررة" in text:
        archive_loc = "دار المحفوظات العمومية - سجلات المكلفات"
        
    # 2. Ledger type
    ledger_type = "دفاتر المواليد والوفيات"
    if "مكلفة" in text or "أطيان" in text:
        ledger_type = "سجلات مكلفات الأطيان والعقارات"
    elif "وفاة" in text or "وفيات" in text:
        ledger_type = "سجلات الوفيات القديمة"
    elif "ميلاد" in text:
        ledger_type = "دفاتر المواليد الورقية القديمة"

    # 3. Ledger number
    ledger_match = re.search(r'(?:دفتر|سجل)(?:\s*(?:رقم|مكلفة|مواليد|وفيات)?\s*[:\s])\s*(\d+)', text)
    ledger_number = ledger_match.group(1) if ledger_match else None

    # 4. Page number
    page_match = re.search(r'(?:صحيفة|صفحة|ص)\s*(?:رقم)?\s*[:\s]\s*(\d+)', text)
    page_number = page_match.group(1) if page_match else None

    # 5. Year
    year_match = re.search(r'(?:لسنة|عام|سنة)\s*[:\s]?\s*(18\d{2}|19\d{2}|20\d{2})', text)
    registration_year = year_match.group(1) if year_match else None

    # 6. Governorate
    gov_match = re.search(r'(?:محافظة|مديرية)\s*[:\s]\s*([^\n|،]+)', text)
    governorate = gov_match.group(1).strip() if gov_match else None

    # 7. District / Kesm / Markaz
    district_match = re.search(r'(?:مركز|قسم|بندر)\s*[:\s]\s*([^\n|،]+)', text)
    district_kesm = district_match.group(1).strip() if district_match else None

    # 8. Person Name
    name_match = re.search(r'(?:اسم المولود|اسم المتوفى|المكلف باسمه|الاسم)\s*[:\s]\s*([^\n|،]+)', text)
    if name_match:
        person_name = name_match.group(1).strip()
    else:
        # Fallback to general line
        person_name = "غير محدد بدقة من النص"

    # 9. Father Name
    father_match = re.search(r'(?:اسم الوالد|والده)\s*[:\s]\s*([^\n|،]+)', text)
    father_name = father_match.group(1).strip() if father_match else None

    # 10. Mother Name
    mother_match = re.search(r'(?:اسم الوالدة|والدته)\s*[:\s]\s*([^\n|،]+)', text)
    mother_name = mother_match.group(1).strip() if mother_match else None

    # 11. Event date
    date_match = re.search(r'(?:تاريخ الولادة|تاريخ الوفاة|تاريخ الواقعة|بتاريخ)\s*[:\s]\s*([^\n|،]+)', text)
    event_date = date_match.group(1).strip() if date_match else None

    # 12. Stamps / Seals
    stamps = []
    if "شعار الجمهورية" in text or "النسر" in text or "خاتم" in text:
        stamps.append("خاتم شعار الجمهورية (النسر)")
    if "الأحوال المدنية" in text:
        stamps.append("ختم الإدارة العامة للأحوال المدنية")
    if "دار المحفوظات" in text:
        stamps.append("ختم مصلحة دار المحفوظات العمومية")
    official_stamps = " / ".join(stamps) if stamps else "لا توجد أختام واضحة بالنص"

    # Compute confidence
    score = 0.40
    if person_name and person_name != "غير محدد بدقة من النص":
        score += 0.15
    if ledger_number:
        score += 0.15
    if registration_year:
        score += 0.10
    if governorate or district_kesm:
        score += 0.10
    if "ختم" in text or "شعار الجمهورية" in text:
        score += 0.10

    score = min(round(score, 2), 0.98)

    now = datetime.utcnow().isoformat()
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO extracted_ledgers (
        document_title, archive_location, ledger_type, ledger_number, page_number,
        registration_year, district_kesm, governorate, person_name, father_name,
        mother_name, event_date, official_stamps, confidence_score, raw_text, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_title, archive_loc, ledger_type, ledger_number, page_number,
        registration_year, district_kesm, governorate, person_name, father_name,
        mother_name, event_date, official_stamps, score, text, now
    ))
    db.commit()
    record_id = cursor.lastrowid

    return ExtractedRecord(
        id=record_id,
        document_title=doc_title,
        archive_location=archive_loc,
        ledger_type=ledger_type,
        ledger_number=ledger_number,
        page_number=page_number,
        registration_year=registration_year,
        district_kesm=district_kesm,
        governorate=governorate,
        person_name=person_name,
        father_name=father_name,
        mother_name=mother_name,
        event_date=event_date,
        official_stamps=official_stamps,
        confidence_score=score,
        raw_text=text,
        created_at=now
    )

@router.get("/records", response_model=List[ExtractedRecord])
def list_extracted_records(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM extracted_ledgers ORDER BY id DESC")
    rows = cursor.fetchall()
    
    records = []
    for r in rows:
        records.append(ExtractedRecord(
            id=r["id"],
            document_title=r["document_title"],
            archive_location=r["archive_location"],
            ledger_type=r["ledger_type"],
            ledger_number=r["ledger_number"],
            page_number=r["page_number"],
            registration_year=r["registration_year"],
            district_kesm=r["district_kesm"],
            governorate=r["governorate"],
            person_name=r["person_name"],
            father_name=r["father_name"],
            mother_name=r["mother_name"],
            event_date=r["event_date"],
            official_stamps=r["official_stamps"],
            confidence_score=r["confidence_score"],
            raw_text=r["raw_text"],
            created_at=r["created_at"]
        ))
    return records
