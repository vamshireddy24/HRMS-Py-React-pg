# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.security import hash_password
from app.services import audit_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password required")
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": str(user.id), "org_id": str(user.org_id)})
    # record audit
    audit_service.record(db, user.org_id, user.id, "login", resource_type="user", resource_id=user.id, details={"email": user.email})
    db.commit()
    return {"access_token": token, "token_type": "bearer"}

# Optional register/create user endpoint (requires admin)
@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # THIS endpoint is intended for demo/testing only. Real projects should protect it.
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    # no org in payload; in practice include org_id or restrict this flow
    # For demo we'll create a user without org (not ideal)
    hashed = hash_password(payload.password)
    user = User(org_id=None, email=payload.email, password_hash=hashed, full_name=payload.full_name, role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": str(user.id), "email": user.email}
