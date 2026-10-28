"""
FastAPI entrypoint. Exposes a health-check endpoint and basic lead storage —
chat/LLM routes will be added in a later slice.
"""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.db import Base, engine, get_db
from app.models import Lead
from app.schemas import LeadCreate, LeadRead

app = FastAPI(title="Buyer Intake Assistant API")

# Restricted to the frontend's dev origin so a browser-based client can call
# this API locally. Widen/replace this once the app is deployed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/leads", response_model=LeadRead, status_code=201)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.get("/leads", response_model=list[LeadRead])
def list_leads(db: Session = Depends(get_db)):
    return db.query(Lead).order_by(Lead.created_at.desc()).all()
