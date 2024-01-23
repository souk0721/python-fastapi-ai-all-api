from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from packages.database.models import User
from packages.database.db import get_db
from sqlalchemy.orm import Session

# 환경 설정 파일로부터 필요한 설정 가져오기
from dotenv import dotenv_values

config = dotenv_values(".env")
# JWT 토큰 설정
SECRET_KEY = config.get('SECRET_KEY')   
ALGORITHM = config.get('ALGORITHM')  

# 패스워드 해싱을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT 토큰 생성 함수
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 패스워드 검증 함수
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 패스워드 해싱 함수
def get_password_hash(password):
    return pwd_context.hash(password)

# 인증된 사용자 가져오는 함수
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
