from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import sqlite3
from datetime import datetime
from app.database import get_db
from app.schemas import CaseCreate, CaseUpdate, CaseResponse

router = APIRouter(prefix="/api/cases", tags=["Cases"])

@router.get("", response_model=List[CaseResponse])
def list_cases(
    status: Optional[str] = None,
    case_type: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    query = "SELECT * FROM cases WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    if case_type:
        query += " AND case_type LIKE ?"
        params.append(f"%{case_type}%")
        
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    cases = []
    for r in rows:
        cases.append(CaseResponse(
            id=r["id"],
            client_name=r["client_name"],
            case_type=r["case_type"],
            national_id=r["national_id"],
            poa_number=r["poa_number"],
            poa_date=r["poa_date"],
            poa_expiry=r["poa_expiry"],
            current_stage=r["current_stage"],
            target_office=r["target_office"],
            status=r["status"],
            notes=r["notes"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        ))
    return cases

@router.post("", response_model=CaseResponse)
def create_case(case_in: CaseCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO cases (
        client_name, case_type, national_id, poa_number, poa_date, poa_expiry,
        current_stage, target_office, status, notes, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_in.client_name,
        case_in.case_type,
        case_in.national_id,
        case_in.poa_number,
        case_in.poa_date,
        case_in.poa_expiry,
        case_in.current_stage,
        case_in.target_office,
        case_in.status,
        case_in.notes,
        now,
        now
    ))
    db.commit()
    new_id = cursor.lastrowid
    
    return CaseResponse(
        id=new_id,
        client_name=case_in.client_name,
        case_type=case_in.case_type,
        national_id=case_in.national_id,
        poa_number=case_in.poa_number,
        poa_date=case_in.poa_date,
        poa_expiry=case_in.poa_expiry,
        current_stage=case_in.current_stage,
        target_office=case_in.target_office,
        status=case_in.status,
        notes=case_in.notes,
        created_at=now,
        updated_at=now
    )

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    r = cursor.fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="Case not found")
        
    return CaseResponse(
        id=r["id"],
        client_name=r["client_name"],
        case_type=r["case_type"],
        national_id=r["national_id"],
        poa_number=r["poa_number"],
        poa_date=r["poa_date"],
        poa_expiry=r["poa_expiry"],
        current_stage=r["current_stage"],
        target_office=r["target_office"],
        status=r["status"],
        notes=r["notes"],
        created_at=r["created_at"],
        updated_at=r["updated_at"]
    )

@router.put("/{case_id}", response_model=CaseResponse)
def update_case(case_id: int, case_in: CaseUpdate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    r = cursor.fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="Case not found")
        
    now = datetime.utcnow().isoformat()
    fields = []
    params = []
    
    for k, v in case_in.dict(exclude_unset=True).items():
        fields.append(f"{k} = ?")
        params.append(v)
        
    if not fields:
        return get_case(case_id, db)
        
    fields.append("updated_at = ?")
    params.append(now)
    params.append(case_id)
    
    cursor.execute(f"UPDATE cases SET {', '.join(fields)} WHERE id = ?", params)
    db.commit()
    
    return get_case(case_id, db)

@router.delete("/{case_id}")
def delete_case(case_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM cases WHERE id = ?", (case_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Case not found")
        
    cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
    db.commit()
    return {"message": "Case deleted successfully", "id": case_id}
