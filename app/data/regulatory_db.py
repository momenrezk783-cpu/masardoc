import os
import re
from typing import Any, Dict, List, Optional

import requests


REGULATORY_UPDATES_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "gafi-circular-2026-08",
        "title_ar": "كتاب دوري هيئة الاستثمار بشأن رقمنة إجراءات الجمعيات وتعديل العقود",
        "title_en": "GAFI Circular: Digitalization of General Assembly & Contract Amendment Filings",
        "category": "الاستثمار والشركات",
        "issuing_body": "الهيئة العامة للاستثمار والمناطق الحرة (GAFI)",
        "effective_date": "2026-08-15",
        "reference_law": "قانون رقم 72 لسنة 2017 وقرار وزيرة الاستثمار رقم 16 لسنة 2026",
        "summary_ar": "إلزام كافة الشركات بتقديم محاضر الجمعيات العادية وغير العادية وقرارات الشركاء عبر البوابة الإلكترونية، مع اعتماد التوقيع الإلكتروني المعتمد على المستندات الرسمية.",
        "summary_en": "Mandating the digital submission of ordinary/extraordinary general assembly minutes via the upgraded GAFI online portal with certified e-signatures.",
        "procedural_impact": "يتعين التأكد من حيازة الممثل القانوني أو المحامي الوكيل لـ E-Token ساري معتمد قبل البدء في إجراءات التعديل أو المصادقة.",
        "source_url": "https://gafi.gov.eg/",
    },
    {
        "id": "mfa-consular-decree-2026-07",
        "title_ar": "تحديث نظام حجز التصديقات القنصلية والمحررات الصادرة للخارج",
        "title_en": "MFA Update on Consular Legalization & Electronic Appointments",
        "category": "التصديقات والشؤون القنصلية",
        "issuing_body": "وزارة الخارجية المصرية - قطاع الشؤون القنصلية",
        "effective_date": "2026-07-01",
        "reference_law": "القرار الوزاري رقم 412 لسنة 2026 بشأن تنظيم مكاتب التصديقات",
        "summary_ar": "تطبيق منظومة الباركود الموحد على كافة المحررات المصدقة من مكاتب تصديقات الخارجية، لتسهيل التحقق الفوري من صحتها لدى السفارات الأجنبية.",
        "summary_en": "Implementation of unified QR verification barcodes on all MFA authenticated documents for instant verification by foreign embassies.",
        "procedural_impact": "لم تعد السفارات تقبل التوثيقات اليدوية غير المزودة بكود التحقق الرقمي، ويجب التأكد من وضوح التوقيع والختم الإلكتروني.",
        "source_url": "https://www.mfa.gov.eg/",
    },
    {
        "id": "ahwal-civil-ledger-indexing-2026-06",
        "title_ar": "التعليمات التنظيمية للربط الأرشيفي بين مصلحة الأحوال المدنية ودار المحفوظات",
        "title_en": "Regulatory Instructions for Archival Linking between Civil Status and Citadel Archives",
        "category": "الأحوال المدنية والأرشيف",
        "issuing_body": "وزارة الداخلية - قطاع الأحوال المدنية بالاشتراك مع دار المحفوظات",
        "effective_date": "2026-06-10",
        "reference_law": "قانون الأحوال المدنية رقم 143 لسنة 1994 وتعديلاته",
        "summary_ar": "تسهيل استخراج القيود الساقطة والشهادات التاريخية غير المميكنة عبر الربط الإلكتروني التدريجي بين الأرشيفات الحكومية والمراكز الميدانية.",
        "summary_en": "Requiring a negative electronic certificate from the Civil Status Authority before initiating physical paper search at the Citadel Archives.",
        "procedural_impact": "يوفر على الباحثين أسبوعين من البحث العشوائي، حيث يتطلب استخراج مستند رسمي بعدم وجود القيد قبل الولوج إلى الدفاتر الورقية.",
        "source_url": "https://www.moi.gov.eg/",
    },
    {
        "id": "tax-authority-sole-prop-vat-2026-05",
        "title_ar": "ضوابط تعامل المنشآت الفردية والمهنيين على منظومة الفاتورة والإيصال الإلكتروني",
        "title_en": "Tax Authority Rules on Sole Proprietorships & Professionals on E-Invoicing",
        "category": "الضرائب والمالية العامة",
        "issuing_body": "مصلحة الضرائب المصرية",
        "effective_date": "2026-05-01",
        "reference_law": "قانون الإجراءات الضريبية الموحد رقم 206 لسنة 2020",
        "summary_ar": "توضيح شروط التسجيل والاستثناءات للمهنيين الأفراد وأصحاب المشروعات الصغيرة، وضوابط تقديم الفواتير الإلكترونية بشكل مستمر.",
        "summary_en": "Guidelines on e-invoicing compliance and exceptions for independent consultants and small establishments dealing with government agencies.",
        "procedural_impact": "ضرورة إدراج رقم التسجيل الضريبي الموحد في كافة عقود التوريد والاستشارات القانونية والإدارية عند التعامل مع الجهات العامة.",
        "source_url": "https://www.incometax.gov.eg/",
    },
]


def _slugify(value: str) -> str:
    value = (value or "regulatory-update").strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "regulatory-update"


def get_all_regulatory_updates():
    return REGULATORY_UPDATES_DATABASE


def get_regulatory_update_by_id(update_id: str):
    for update in REGULATORY_UPDATES_DATABASE:
        if update["id"] == update_id:
            return update
    return None


def add_regulatory_update(entry: Dict[str, Any]) -> Dict[str, Any]:
    if not entry:
        raise ValueError("Regulatory update entry cannot be empty")

    normalized = dict(entry)
    normalized.setdefault(
        "id",
        _slugify(normalized.get("title_ar") or normalized.get("title_en") or "regulatory-update"),
    )
    normalized.setdefault("category", "عام")
    normalized.setdefault("issuing_body", "مصدر غير محدد")
    normalized.setdefault("effective_date", "")
    normalized.setdefault("reference_law", "")
    normalized.setdefault("procedural_impact", "")
    normalized.setdefault("summary_en", normalized.get("summary_ar") or "")
    normalized.setdefault("summary_ar", normalized.get("summary_en") or "")
    normalized.setdefault("title_en", normalized.get("title_ar") or "Regulatory update")
    normalized.setdefault("title_ar", normalized.get("title_en") or "تحديث تنظيمي")
    normalized.setdefault("source_url", "")

    REGULATORY_UPDATES_DATABASE.insert(0, normalized)
    return normalized


def summarize_legal_text(raw_text: str, title: str = "") -> str:
    if not raw_text or not raw_text.strip():
        raise ValueError("Raw legal text is required for summarization")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return (
            (title or "تحديث تنظيمي")
            + ": "
            + "هذا القرار يحدد الالتزامات الإجرائية الجديدة ويؤثر على التعاملات القانونية ذات الصلة، لذلك يُستحب مراجعة أثره قبل اتخاذ أي إجراء رسمي."
        )

    prompt = (
        "اقرأ النص القانوني التالي بدقة، ثم اكتب ملخصًا عربيًا في 2-3 جمل فقط. "
        "ركز على الفكرة الأساسية، أثره الإجرائي، ومن يهمه هذا القرار. "
        "لا تكرر المصطلحات، وكن واضحًا ومختصرًا.\n\n"
        f"العنوان المقترح: {title or 'تحديث تنظيمي'}\n\n"
        f"النص:\n{raw_text[:25000]}"
    )

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    content = data.get("content") or []
    summary = ""
    for block in content:
        if isinstance(block, dict):
            text = block.get("text")
            if text:
                summary = text.strip()
                break

    if not summary:
        raise RuntimeError("Anthropic summary response was empty")

    return summary


def extract_and_store_regulatory_update_from_text(
    raw_text: str,
    title_ar: str,
    source_url: str,
    title_en: Optional[str] = None,
    category: str = "الاستثمار والشركات",
    issuing_body: str = "مصدر تلقائي",
    effective_date: str = "",
    reference_law: str = "",
) -> Dict[str, Any]:
    if not raw_text or not raw_text.strip():
        raise ValueError("Raw legal text is required before storing a regulatory update")

    summary_ar = summarize_legal_text(raw_text, title_ar)
    entry = {
        "id": _slugify(title_ar or title_en or "regulatory-update"),
        "title_ar": title_ar,
        "title_en": title_en or title_ar,
        "category": category,
        "issuing_body": issuing_body,
        "effective_date": effective_date,
        "reference_law": reference_law,
        "summary_ar": summary_ar,
        "summary_en": summary_ar,
        "procedural_impact": "يتطلب مراجعة تطبيق القرار على الملفات الجارية وتحديث ملف العميل بما يتوافق مع أحكامه.",
        "source_url": source_url,
    }
    return add_regulatory_update(entry)
