from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CaseBase(BaseModel):
    client_name: str = Field(..., example="ورثة المرحوم فؤاد إبراهيم")
    case_type: str = Field(..., example="استخراج قيود من دار المحفوظات بالقلعة")
    national_id: Optional[str] = Field(None, example="29607231201234")
    poa_number: Optional[str] = Field(None, example="توكيل خاص 883 لسنة 2026")
    poa_date: Optional[str] = Field(None, example="2026-02-15")
    poa_expiry: Optional[str] = Field(None, example="2027-02-15")
    current_stage: str = Field(default="Initial Review", example="البحث بالدفاتر الورقية")
    target_office: Optional[str] = Field(None, example="دار المحفوظات العمومية - القلعة")
    status: str = Field(default="In Progress", example="In Progress")
    notes: Optional[str] = Field(None, example="تم تسديد الرسوم وتحديد المجلد رقم 4")

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    client_name: Optional[str] = None
    case_type: Optional[str] = None
    national_id: Optional[str] = None
    poa_number: Optional[str] = None
    poa_date: Optional[str] = None
    poa_expiry: Optional[str] = None
    current_stage: Optional[str] = None
    target_office: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class CaseResponse(CaseBase):
    id: int
    created_at: str
    updated_at: str

class ProcedureStep(BaseModel):
    step_number: int
    title_ar: str
    title_en: str
    location: str
    department: str
    description_ar: str
    description_en: str
    required_documents: List[str]
    poa_requirements: Optional[str] = None
    estimated_duration: str
    official_fees: str
    critical_tips: List[str]

class ProcedureDetail(BaseModel):
    id: str
    title_ar: str
    title_en: str
    category: str
    overview_ar: str
    overview_en: str
    target_authority: str
    recommended_poa_text: str
    steps: List[ProcedureStep]
    statutory_basis: str

class LedgerExtractionRequest(BaseModel):
    document_title: str
    raw_text: Optional[str] = None
    ledger_image_base64: Optional[str] = None

class ExtractedRecord(BaseModel):
    id: Optional[int] = None
    document_title: str
    archive_location: str
    ledger_type: str
    ledger_number: Optional[str]
    page_number: Optional[str]
    registration_year: Optional[str]
    district_kesm: Optional[str]
    governorate: Optional[str]
    person_name: str
    father_name: Optional[str]
    mother_name: Optional[str]
    event_date: Optional[str]
    official_stamps: Optional[str]
    confidence_score: float
    raw_text: Optional[str]
    created_at: Optional[str]

class RegulatoryUpdate(BaseModel):
    id: str
    title_ar: str
    title_en: str
    category: str
    issuing_body: str
    effective_date: str
    summary_ar: str
    summary_en: str
    reference_law: str
    procedural_impact: str
