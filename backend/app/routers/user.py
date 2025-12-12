# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user_schema import UserCreate, UserOut
from app.models.user import User
from app.core.security import hash_password
from app.services import audit_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed = hash_password(payload.password)
    user = User(org_id=current_user.org_id, email=payload.email, password_hash=hashed, full_name=payload.full_name, role="user")
    db.add(user)
    db.flush()
    audit_service.record(db, current_user.org_id, current_user.id, "user_create", resource_type="user", resource_id=user.id, details={"email": user.email})
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserOut)
def me(current_user = Depends(get_current_user)):
    return current_user
