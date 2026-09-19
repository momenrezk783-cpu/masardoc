from typing import Optional

from fastapi import APIRouter, HTTPException

from app.data.regulatory_db import (
    get_all_regulatory_updates,
    get_regulatory_update_by_id,
    extract_and_store_regulatory_update_from_text,
)
from app.schemas import RegulatoryUpdate
from scrapers.regulatory_radar.poc_scraper import scrape_and_store_regulatory_update

router = APIRouter(prefix="/api/regulatory", tags=["Regulatory Radar"])


@router.get("", response_model=list[RegulatoryUpdate])
def list_regulatory_updates(
    category: Optional[str] = None,
    query: Optional[str] = None,
):
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
def create_regulatory_update_from_source(
    source_url: str,
    title_ar: Optional[str] = None,
    title_en: Optional[str] = None,
    category: Optional[str] = None,
    issuing_body: Optional[str] = None,
    effective_date: Optional[str] = None,
    reference_law: Optional[str] = None,
):
    if not source_url:
        raise HTTPException(status_code=400, detail="source_url is required")

    try:
        result = scrape_and_store_regulatory_update(
            target_url=source_url,
            title_ar=title_ar or "تحديث تنظيمي جديد تم جمعه تلقائيًا",
            title_en=title_en or "New regulatory update summarized automatically",
            category=category or "الاستثمار والشركات",
            issuing_body=issuing_body or "مصدر تلقائي",
            effective_date=effective_date or "",
            reference_law=reference_law or "",
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(
            status_code=500,
            detail=f"Failed to scrape and summarize legal update: {exc}",
        ) from exc
