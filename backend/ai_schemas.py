from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas import JourneyResponse

class AIJourneyRequest(BaseModel):
    origin: str = Field(..., description="The starting location or stop name mentioned by the user")
    destination: str = Field(..., description="The destination location or stop name mentioned by the user")
    time: Optional[str] = Field(None, description="The requested departure or arrival time (e.g., '5pm', 'tomorrow morning'). If not specified, use 'now'.")
    optimization: str = Field("fastest", description="The optimization goal, usually 'fastest' or 'fewest_transfers'.")
    max_transfers: Optional[int] = Field(None, description="The maximum number of transfers the user is willing to make.")

class AIChatRequest(BaseModel):
    user_query: str
    journey_results: Optional[JourneyResponse] = None

class AIResolutionRequest(BaseModel):
    query: str = Field(..., description="The location name to resolve to a stop_id")

class AIResolutionResponse(BaseModel):
    stop_id: Optional[str] = Field(None, description="The resolved stop_id if a unique match is found")
    ambiguous: bool = Field(False, description="True if multiple possible stops were found")
    suggestions: List[str] = Field(default_factory=list, description="List of possible stop names if ambiguous or not found")
    found: bool = Field(False, description="True if any match was found")
