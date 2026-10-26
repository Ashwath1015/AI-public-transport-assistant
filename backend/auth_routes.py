from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import auth_schemas, auth_models, auth_service
from database import get_db
from auth_service import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=auth_schemas.UserResponse)
async def register(user_in: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(auth_models.User).filter(auth_models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = auth_service.get_password_hash(user_in.password)
    new_user = auth_models.User(
        email=user_in.email,
        hashed_password=hashed_pwd,
        full_name=user_in.full_name,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user_in: auth_schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(auth_models.User).filter(auth_models.User.email == user_in.email).first()
    if not user or not auth_service.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
