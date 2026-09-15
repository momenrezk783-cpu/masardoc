from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.data.regulatory_db import get_all_regulatory_updates, get_regulatory_update_by_id
from app.schemas import RegulatoryUpdate

router = APIRouter(prefix="/api/regulatory", tags=["Regulatory Radar"])

@router.get("", response_model=List[RegulatoryUpdate])
def list_regulatory_updates(
    category: Optional[str] = None,
    query: Optional[str] = None
):
    updates = get_all_regulatory_updates()
    if category:
        updates = [u for u in updates if u.get("category") == category]
    if query:
        q = query.lower()
        updates = [
            u for u in updates 
            if q in u.get("title_ar", "").lower() 
            or q in u.get("title_en", "").lower()
            or q in u.get("summary_ar", "").lower()
            or q in u.get("issuing_body", "").lower()
        ]
    return updates

@router.get("/{update_id}", response_model=RegulatoryUpdate)
def get_regulatory_update(update_id: str):
    u = get_regulatory_update_by_id(update_id)
    if not u:
        raise HTTPException(status_code=404, detail="Regulatory update not found")
    return u
