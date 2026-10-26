from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import crud
import schemas
import ai_service
from ai_schemas import AIChatRequest
from auth_routes import router as auth_router
from user_routes import router as user_router
from admin_routes import router as admin_router

app = FastAPI(title="Chennai Transit Planner API")

# CORS Middleware - Allowing all origins for maximum compatibility during demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/stops/search", response_model=List[schemas.StopResponse])
async def search_stops(
    q: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    radius: Optional[int] = Query(500),
    limit: Optional[int] = Query(10),
    db: Session = Depends(get_db)
):
    return crud.search_stops(db, q=q, lat=lat, lon=lon, radius=radius, limit=limit)

@app.post("/api/journeys/search", response_model=schemas.JourneyResponse)
async def search_journeys(
    request: schemas.JourneyRequest,
    db: Session = Depends(get_db)
):
    journey = crud.search_journeys(db, request)
    if not journey:
        raise HTTPException(status_code=404, detail="No journey found between the specified stops")
    return journey

@app.post("/api/assistant/parse")
async def parse_natural_language(
    user_text: str,
    db: Session = Depends(get_db)
):
    """
    Turns natural language into validated routing parameters.
    """
    result = ai_service.process_ai_request(db, user_text)
    if result["status"] != "validated":
        return result
    return result

@app.post("/api/assistant/chat")
async def assistant_chat(
    request: AIChatRequest,
    db: Session = Depends(get_db)
):
    """
    Explains routing results in natural language.
    """
    try:
        explanation = ai_service.explain_journey(request.user_query, request.journey_results)
        return {"response": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
