# app/services/audit_service.py
from app.models.log import Log

def record(db, org_id, user_id, action: str, resource_type: str = None, resource_id = None, details = None, meta = None):
    entry = Log(org_id=org_id, user_id=user_id, action=action, resource_type=resource_type, resource_id=resource_id, details=details, meta=meta)
    db.add(entry)
    # commit is handled by caller