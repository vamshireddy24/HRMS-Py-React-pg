# app/schemas/organisation_schema.py
from pydantic import BaseModel

class OrganisationCreate(BaseModel):
    name: str

class OrganisationOut(BaseModel):
    id: str
    name: str
    created_at: str

    class Config:
        orm_mode = True
