# app/routers/log.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.models.log import Log
from app.schemas.log_schema import LogOut

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("", response_model=List[LogOut])
def list_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user), limit: int = 100, offset: int = 0):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view logs")
    q = db.query(Log).filter(Log.org_id == current_user.org_id).order_by(Log.timestamp.desc()).offset(offset).limit(limit)
    return q.all()
