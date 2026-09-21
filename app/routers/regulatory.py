from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.data.regulatory_db import (
    get_all_regulatory_updates,
    get_regulatory_update_by_id,
)
from app.schemas import RegulatoryUpdate
from scrapers.regulatory_radar.poc_scraper import scrape_and_store_regulatory_update

router = APIRouter(prefix="/api/regulatory", tags=["Regulatory Radar"])


class RegulatoryScrapeRequest(BaseModel):
    source_url: HttpUrl
    title_ar: Optional[str] = None
    title_en: Optional[str] = None
    category: Optional[str] = None
    issuing_body: Optional[str] = None
    effective_date: Optional[str] = None
    reference_law: Optional[str] = None


@router.get("", response_model=list[RegulatoryUpdate])
def list_regulatory_updates(category: Optional[str] = None, query: Optional[str] = None):
    updates = get_all_regulatory_updates()
    if category:
        updates = [u for u in updates if u.get("category") == category]
    if query:
        q = query.lower()
        updates = [
            u for u in updates
            if q in (u.get("title_ar") or "").lower()
            or q in (u.get("title_en") or "").lower()
            or q in (u.get("summary_ar") or "").lower()
            or q in (u.get("issuing_body") or "").lower()
        ]
    return updates


@router.get("/{update_id}", response_model=RegulatoryUpdate)
def get_regulatory_update(update_id: str):
    update = get_regulatory_update_by_id(update_id)
    if not update:
        raise HTTPException(status_code=404, detail="Regulatory update not found")
    return update


@router.post("/scrape-and-summarize", response_model=RegulatoryUpdate)
def create_regulatory_update_from_source(payload: RegulatoryScrapeRequest):
    """Manually fetch, summarize, and add one regulatory update."""
    try:
        return scrape_and_store_regulatory_update(
            target_url=str(payload.source_url),
            title_ar=payload.title_ar or "تحديث تنظيمي جديد تم جمعه يدويًا",
            title_en=payload.title_en or "Manually collected regulatory update",
            category=payload.category or "الاستثمار والشركات",
            issuing_body=payload.issuing_body or "مصدر يدوي",
            effective_date=payload.effective_date or "",
            reference_law=payload.reference_law or "",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to scrape source: {exc}") from exc
