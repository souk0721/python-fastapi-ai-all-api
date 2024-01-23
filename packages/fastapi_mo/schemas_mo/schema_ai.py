from pydantic import BaseModel


# Pydantic 모델 정의
class Ai(BaseModel):
    q: str


    