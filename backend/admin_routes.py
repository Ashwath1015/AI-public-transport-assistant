from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import admin_schemas, auth_service
from database import get_db
from auth_service import get_current_user, check_admin_role
from auth_models import User

router = APIRouter(prefix="/api/admin", tags=["Administration"])

async def get_admin_user(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    check_admin_role(user.role)
    return user

@router.post("/import", response_model=admin_schemas.ImportStatus)
async def trigger_import(request: admin_schemas.DataImportRequest, admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    """
    Triggers the GTFS importer script.
    """
    # In a real implementation, this would call the importer.py logic
    # For the demo, we return a mock status
    return {
        "status": "success",
        "records_processed": 1250,
        "errors": []
    }

@router.get("/health", response_model=admin_schemas.SystemHealthResponse)
async def get_system_health(admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    """
    Checks data freshness and system status.
    """
    # Mock health check
    return {
        "database_connected": True,
        "last_import_date": "2026-10-20T10:00:00Z",
        "data_freshness": "Up to date",
        "alerts": ["Minor latency in PostGIS spatial queries"]
    }

@router.get("/users", response_model=List[admin_schemas.UserResponse])
async def list_users(admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(User).all()
