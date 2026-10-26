from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FavoriteResponse(BaseModel):
    stop_id: str
    stop_name: str

class HistoryResponse(BaseModel):
    id: int
    origin_id: str
    destination_id: str
    created_at: datetime

class PreferenceResponse(BaseModel):
    optimization: str
    max_transfers: int
    notification_enabled: bool

class FavoriteCreate(BaseModel):
    stop_id: str
    stop_name: str

class PreferenceUpdate(BaseModel):
    optimization: Optional[str] = None
    max_transfers: Optional[int] = None
    notification_enabled: Optional[bool] = None
