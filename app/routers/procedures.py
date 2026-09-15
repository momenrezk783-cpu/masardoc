from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.data.procedures_db import get_all_procedures, get_procedure_by_id
from app.schemas import ProcedureDetail

router = APIRouter(prefix="/api/procedures", tags=["Procedures"])

@router.get("", response_model=List[ProcedureDetail])
def list_procedures(category: Optional[str] = None):
    procedures = get_all_procedures()
    if category:
        procedures = [p for p in procedures if p.get("category") == category]
    return procedures

@router.get("/{proc_id}", response_model=ProcedureDetail)
def get_procedure(proc_id: str):
    proc = get_procedure_by_id(proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return proc

@router.get("/{proc_id}/poa-template")
def get_poa_template(proc_id: str, client_name: Optional[str] = None, attorney_name: Optional[str] = None):
    proc = get_procedure_by_id(proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procedure not found")
    
    client = client_name or "[اسم الموكل / العميل]"
    attorney = attorney_name or "[اسم الأستاذ الوكيل / المحامي]"
    
    raw_text = proc.get("recommended_poa_text", "")
    full_clause = (
        f"أنا الموقع أدناه: {client}، بصفتي (أصيل / ممثل قانوني)، قد وكلت بموجب هذا: {attorney} "
        f"في الآتي:\n\"{raw_text}\"\n"
        f"وله في سبيل ذلك التوقيع نيابة عني واستلام المحررات الرسمية ودفع الرسوم المقررة والطعن والتقرير بما يلزم قانوناً."
    )
    
    return {
        "procedure_id": proc_id,
        "procedure_title_ar": proc["title_ar"],
        "target_authority": proc["target_authority"],
        "poa_clause": full_clause,
        "raw_stipulation": raw_text
    }
