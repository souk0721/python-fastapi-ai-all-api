from pydantic import BaseModel


# Pydantic 모델 정의
class VideoCreate(BaseModel):
    youtube_url: str


    