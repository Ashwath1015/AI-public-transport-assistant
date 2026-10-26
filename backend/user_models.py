from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from auth_models import User

Base = declarative_base()

class UserFavorite(Base):
    __tablename__ = "user_favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stop_id = Column(String, nullable=False)
    stop_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserJourneyHistory(Base):
    __tablename__ = "user_journey_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    origin_id = Column(String, nullable=False)
    destination_id = Column(String, nullable=False)
    departure_time = Column(Integer)
    journey_data = Column(JSON) # Store the full response for quick recall
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    optimization = Column(String, default="fastest")
    max_transfers = Column(Integer, default=3)
    notification_enabled = Column(Integer, default=1) # 1 for true, 0 for false
