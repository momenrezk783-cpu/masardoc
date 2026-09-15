from typing import List, Dict, Any

REGULATORY_UPDATES_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "gafi-circular-2026-08",
        "title_ar": "كتاب دوري هيئة الاستثمار بشأن رقمنة إجراءات الجمعيات وتعديل العقود",
        "title_en": "GAFI Circular: Digitalization of General Assembly & Contract Amendment Filings",
        "category": "الاستثمار والشركات",
        "issuing_body": "الهيئة العامة للاستثمار والمناطق الحرة (GAFI)",
        "effective_date": "2026-08-15",
        "reference_law": "قانون رقم 72 لسنة 2017 وقرار وزيرة الاستثمار رقم 16 لسنة 2026",
        "summary_ar": "إلزام كافة الشركات بتقديم محاضر الجمعيات العادية وغير العادية وقرارات الشركاء عبر البوابة الإلكترونية المحدثة لمراكز خدمات المستثمرين مع إلزامية اعتماد المحاضر بالتوقيع الإلكتروني للمفوض.",
        "summary_en": "Mandating the digital submission of ordinary/extraordinary general assembly minutes via the upgraded GAFI online portal with certified e-signatures.",
        "procedural_impact": "يتعين التأكد من حيازة الممثل القانوني أو المحامي الوكيل لـ E-Token ساري معتمد قبل البدء في إجراءات تعديل العقود أو الجمعيات."
    },
    {
        "id": "mfa-consular-decree-2026-07",
        "title_ar": "تحديث نظام حجز التصديقات القنصلية والمحررات الصادرة للخارج",
        "title_en": "MFA Update on Consular Legalization & Electronic Appointments",
        "category": "التصديقات والشؤون القنصلية",
        "issuing_body": "وزارة الخارجية المصرية - قطاع الشؤون القنصلية",
        "effective_date": "2026-07-01",
        "reference_law": "القرار الوزاري رقم 412 لسنة 2026 بشأن تنظيم مكاتب التصديقات",
        "summary_ar": "تطبيق منظومة الباركود الموحد على كافة المحررات المصدقة من مكاتب تصديقات الخارجية (أحمد عرابي، الترجمان، المهندسين) للتحقق الفوري من صحة المستندات لدى السفارات الأوروبية والأجنبية.",
        "summary_en": "Implementation of unified QR verification barcodes on all MFA authenticated documents for instant verification by foreign embassies.",
        "procedural_impact": "لم تعد السفارات تقبل التوثيقات اليدوية غير المزودة بكود التحقق الرقمي، ويجب التأكد من وضوح طباعة الباركود عند الاستلام."
    },
    {
        "id": "ahwal-civil-ledger-indexing-2026-06",
        "title_ar": "التعليمات التنظيمية للربط الأرشيفي بين مصلحة الأحوال المدنية ودار المحفوظات",
        "title_en": "Regulatory Instructions for Archival Linking between Civil Status and Citadel Archives",
        "category": "الأحوال المدنية والأرشيف",
        "issuing_body": "وزارة الداخلية - قطاع الأحوال المدنية بالاشتراك مع دار المحفوظات",
        "effective_date": "2026-06-10",
        "reference_law": "قانون الأحوال المدنية رقم 143 لسنة 1994 وتعديلاته",
        "summary_ar": "تسهيل استخراج القيود الساقطة والشهادات التاريخية غير المميكنة عبر الربط الإلكتروني التدريجي، وإلزام المتقدم بتقديم شهادة سلبية من الأحوال المدنية قبل توجيهه لدار المحفوظات بالقلعة.",
        "summary_en": "Requiring a negative electronic certificate from the Civil Status Authority before initiating physical paper search at the Citadel Archives.",
        "procedural_impact": "يوفر على الباحثين أسبوعين من البحث العشوائي، حيث يتطلب استخراج مستند رسمي بعدم وجود القيد إلكترونياً أولاً كشرط قبول طلب دار المحفوظات."
    },
    {
        "id": "tax-authority-sole-prop-vat-2026-05",
        "title_ar": "ضوابط تعامل المنشآت الفردية والمهنيين على منظومة الفاتورة والإيصال الإلكتروني",
        "title_en": "Tax Authority Rules on Sole Proprietorships & Professionals on E-Invoicing",
        "category": "الضرائب والمالية العامة",
        "issuing_body": "مصلحة الضرائب المصرية",
        "effective_date": "2026-05-01",
        "reference_law": "قانون الإجراءات الضريبية الموحد رقم 206 لسنة 2020",
        "summary_ar": "توضيح شروط التسجيل والاستثناءات للمهنيين الأفراد وأصحاب المشروعات الصغيرة، وضوابط تقديم الخدمات للجهات الحكومية والشركات المساهمة.",
        "summary_en": "Guidelines on e-invoicing compliance and exceptions for independent consultants and small establishments dealing with government agencies.",
        "procedural_impact": "ضرورة إدراج رقم التسجيل الضريبي الموحد في كافة عقود التوريد والاستشارات القانونية والإدارية."
    }
]

def get_all_regulatory_updates():
    return REGULATORY_UPDATES_DATABASE

def get_regulatory_update_by_id(update_id: str):
    for u in REGULATORY_UPDATES_DATABASE:
        if u["id"] == update_id:
            return u
    return None
