from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DataImportRequest(BaseModel):
    file_path: str
    data_type: str # e.g., "gtfs", "stops"

class ImportStatus(BaseModel):
    status: str
    records_processed: int
    errors: List[str]

class SystemHealthResponse(BaseModel):
    database_connected: bool
    last_import_date: datetime
    data_freshness: str # e.g., "Up to date", "Outdated"
    alerts: List[str]

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
