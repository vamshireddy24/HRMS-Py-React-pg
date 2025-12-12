from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db
from app.routers import auth, organisation, user

app = FastAPI(title="HRMS API")

# CORS - allow frontend dev origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include all routers
app.include_router(auth.router)
app.include_router(organisation.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "FastAPI backend is running successfully!"}

@app.on_event("startup")
def on_startup():
    # create tables (for development/demo). Use Alembic in prod.
    init_db()