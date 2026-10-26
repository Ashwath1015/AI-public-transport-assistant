from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import user_models, user_schemas, auth_service
from database import get_db
from auth_service import get_current_user

router = APIRouter(prefix="/api/user", tags=["User Personalization"])

# Dependency to get the actual user object from DB based on JWT email
def get_user_by_token(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    from auth_models import User
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/favorites", response_model=List[user_schemas.FavoriteResponse])
async def get_favorites(user=Depends(get_user_by_token), db: Session = Depends(get_db)):
    return db.query(user_models.UserFavorite).filter(user_models.UserFavorite.user_id == user.id).all()

@router.post("/favorites")
async def add_favorite(fav: user_schemas.FavoriteCreate, user=Depends(get_user_by_token), db: Session = Depends(get_db)):
    db_fav = user_models.UserFavorite(user_id=user.id, stop_id=fav.stop_id, stop_name=fav.stop_name)
    db.add(db_fav)
    db.commit()
    return {"status": "added"}

@router.get("/history", response_model=List[user_schemas.HistoryResponse])
async def get_history(user=Depends(get_user_by_token), db: Session = Depends(get_db)):
    return db.query(user_models.UserJourneyHistory).filter(user_models.UserJourneyHistory.user_id == user.id).all()

@router.get("/preferences", response_model=user_schemas.PreferenceResponse)
async def get_preferences(user=Depends(get_user_by_token), db: Session = Depends(get_db)):
    pref = db.query(user_models.UserPreference).filter(user_models.UserPreference.user_id == user.id).first()
    if not pref:
        # Return defaults if not set
        return {"optimization": "fastest", "max_transfers": 3, "notification_enabled": True}
    return pref

@router.patch("/preferences")
async def update_preferences(pref_in: user_schemas.PreferenceUpdate, user=Depends(get_user_by_token), db: Session = Depends(get_db)):
    pref = db.query(user_models.UserPreference).filter(user_models.UserPreference.user_id == user.id).first()
    if not pref:
        pref = user_models.UserPreference(user_id=user.id)
        db.add(pref)

    if pref_in.optimization: pref.optimization = pref_in.optimization
    if pref_in.max_transfers is not None: pref.max_transfers = pref_in.max_transfers
    if pref_in.notification_enabled is not None: pref.notification_enabled = int(pref_in.notification_enabled)

    db.commit()
    return {"status": "updated"}
