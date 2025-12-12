# app/routers/organisation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.organisation_schema import OrganisationCreate, OrganisationOut
from app.models.organisation import Organisation
from app.models.user import User
from app.core.security import hash_password
from app.services import audit_service

router = APIRouter(prefix="/orgs", tags=["organisations"])

@router.post("", response_model=OrganisationOut)
def create_org(payload: OrganisationCreate, db: Session = Depends(get_db)):
    # create organisation
    existing = db.query(Organisation).filter(Organisation.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organisation exists")
    org = Organisation(name=payload.name)
    db.add(org)
    db.flush()
    # create admin user auto (demo)
    admin_email = f"admin@{payload.name.replace(' ','').lower()}.local"
    admin_password = "admin"  # demo only — change in production
    admin = User(org_id=org.id, email=admin_email, password_hash=hash_password(admin_password), full_name="Org Admin", role="admin")
    db.add(admin)
    audit_service.record(db, org.id, admin.id, "org_create", resource_type="organisation", resource_id=org.id, details={"org_name": org.name})
    db.commit()
    db.refresh(org)
    return org

@router.get("/me")
def get_my_org(user = Depends(get_current_user)):
    # returns organisation id via user
    return {"org_id": str(user.org_id)}
