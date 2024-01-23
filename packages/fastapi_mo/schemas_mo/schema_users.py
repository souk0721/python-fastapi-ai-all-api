from pydantic import BaseModel


# Pydantic 모델 정의
class UserCreate(BaseModel):
    username: str
    password: str
