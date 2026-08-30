from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from database import get_db
from models import Partner
import os

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

ADMIN_KEY = os.getenv("ADMIN_KEY", "allotment-key-admin")

async def get_partner(api_key: str = Security(API_KEY_HEADER), db: Session = Depends(get_db)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required.")
    
    if api_key == ADMIN_KEY:
        return {"id": 0, "name": "Admin", "is_admin": True}
    
    partner = db.query(Partner).filter(
        Partner.api_key == api_key,
        Partner.is_active == True
    ).first()
    
    if not partner:
        raise HTTPException(status_code=403, detail="Invalid or inactive API key.")
    
    return {"id": partner.id, "name": partner.name, "is_admin": False}

async def get_admin(partner = Depends(get_partner)):
    if not partner.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required.")
    return partner