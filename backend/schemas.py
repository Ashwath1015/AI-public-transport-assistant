from pydantic import BaseModel
from typing import Optional, List

class StopResponse(BaseModel):
    stop_id: str
    stop_name: str
    stop_lat: float
    stop_lon: float

    class Config:
        from_attributes = True

class StopSearchQuery(BaseModel):
    q: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius: Optional[int] = 500
    limit: Optional[int] = 10

class JourneyLeg(BaseModel):
    trip_id: str
    route_id: str
    from_stop: str
    from_stop_name: str
    to_stop: str
    to_stop_name: str
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float
    dep_time: str
    arr_time: str

class JourneyResponse(BaseModel):
    total_duration: int
    arrival_time: str
    legs: List[JourneyLeg]

class JourneyRequest(BaseModel):
    origin_id: str
    destination_id: str
    departure_time: int
    optimization: Optional[str] = "fastest"
