from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, status
from packages.database.models import User
from packages.fastapi_mo.security_mo.security import create_access_token, verify_password,get_current_user,pwd_context
from packages.database.db import get_db,SessionLocal
from packages.fastapi_mo.schemas_mo.schema_users import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    session = SessionLocal()
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    secure_data = {
        "message": "This is secure data only for authenticated users.",
        "user": current_user.username
    }
    return secure_data

