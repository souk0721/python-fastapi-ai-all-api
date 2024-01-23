from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Boolean,Text,JSON
from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,declarative_base
import json


Base = declarative_base()


# 사용자 모델
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # YoutubeFile과의 관계 추가
    youtube_files = relationship("YoutubeFile", back_populates="user")

## 원본 파일 저장
class YoutubeFile(Base):
    __tablename__ = "youtube_file"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey 참조 추가
    youtube_url = Column(String, unique=True,nullable=False) # 파일 경로 저장
    title = Column(String) # 파일 경로 저장
    author = Column(String) # 파일 경로 저장
    video_origin_path = Column(String, unique=True,nullable=False) # 파일 경로 저장
    stream_url = Column(String, unique=True,nullable=False) # 파일 경로 저장
    save_folder_path = Column(String, unique=True,nullable=False) # 파일 경로 저장
    is_checked = Column(Boolean, default=False, nullable=False)
    is_complete = Column(Boolean, default=False, nullable=False)
    is_gpt = Column(Boolean, default=False, nullable=False)
    is_gemini = Column(Boolean, default=False, nullable=False)
    is_notion = Column(Boolean, default=False, nullable=False)
    origin_text = Column(Text)
    whisper_json = Column(JSONB, default="", nullable=True)
    ai_title_tag_article = Column(JSON, nullable=True)
    gpt = Column(JSON, nullable=True)
    gemini = Column(JSON, nullable=True)
    notion = Column(JSON, nullable=True)
    gemini_text_failed_count = Column(Integer,default=0)
    gemini_title_tag_failed_count = Column(Integer,default=0)
    
    user = relationship("User", back_populates="youtube_files")
    
    # is_19 = Column(Boolean, default=False, nullable=False)

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "save_folder_path": self.save_folder_path,
    #         "origin_img_path": self.origin_img_path,
    #         "video_json_list": self.video_json_list,
    #         "is_checked": self.is_checked,
    #         "is_complete": self.is_complete,
            
    #     }
## 원본 파일 저장
class RefVideoFile(Base):
    __tablename__ = "ref_video_file"
    
    id = Column(Integer, primary_key=True, index=True)
    # save_folder_path = Column(String, nullable=False) # 파일 경로 저장
    ref_video_path = Column(String, nullable=False) # 파일 경로 저장
    is_checked = Column(Boolean, default=False, nullable=False)
    counted = Column(Integer, default=0, nullable=False)
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         # "save_folder_path": self.save_folder_path,
    #         "ref_video_path": self.ref_video_path,
    #         "is_checked": self.is_checked,
    #         "counted": self.counted,
            
    #     }
        
class OriginTextFile(Base):
    __tablename__ = "origin_text_file"
    
    id = Column(Integer, primary_key=True, index=True)
    youtube_url = Column(String, unique=False) # 파일 경로 저장
    youtube_downfile_path = Column(String(200), default="", nullable=True)
    youtube_title = Column(String(255), default="", nullable=True)
    ai_text = Column(JSON, default="", nullable=True)
    data_json = Column(JSON, default="", nullable=True)
    counted = Column(Integer, default=0, nullable=False)
    is_complete = Column(Boolean, default=False, nullable=False)
    is_youtube = Column(Boolean, default=False, nullable=False)
    # is_19 = Column(Boolean, default=False, nullable=True)
    # is_youtube_check = Column(Boolean, default=False, nullable=True)

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "youtube_url": self.youtube_url,
    #         # "save_folder_path": self.save_folder_path,
    #         # "data_json_list": self.data_json_list,
    #         "counted": self.counted,
    #         "is_complete": self.is_complete,
            
        # }
        
class CompleteVideoFile(Base):
    __tablename__ = "complete_video_file"
    
    id = Column(Integer, primary_key=True, index=True)
    save_folder_path = Column(String, unique=True,nullable=False) # 파일 경로 저장
    complete_video_path = Column(String, unique=True,nullable=False) # 파일 경로 저장
    counted = Column(Integer, default=0, nullable=False)
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "save_folder_path": self.save_folder_path,
    #         "complete_video_path": self.complete_video_path,
    #         "counted": self.counted,
            
    #     }

class CompleteFile(Base):
    __tablename__ = "complete_file"
    
    id = Column(Integer, primary_key=True, index=True)
    save_folder_path = Column(String, unique=True,nullable=False) # 파일 경로 저장
    complete_file_path = Column(String, unique=True,nullable=False) # 파일 경로 저장
    profile = Column(String, default="",nullable=True) # 파일 경로 저장
    title = Column(String, default="", nullable=True)
    is_youtube = Column(Boolean, default=False, nullable=False)
    is_instar = Column(Boolean, default=False, nullable=False)
    is_x = Column(Boolean, default=False, nullable=False)
    is_thread = Column(Boolean, default=False, nullable=False)
    is_pinterest = Column(Boolean, default=False, nullable=False)
    is_fine = Column(Boolean, default=False, nullable=False)
    

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "save_folder_path": self.save_folder_path,
    #         "complete_file_path": self.complete_file_path,
    #         # "data_json_list": self.data_json_list,
    #         "is_youtube": self.is_youtube,
    #         "is_instar": self.is_instar,
    #         "is_x": self.is_x,
    #         "is_thread": self.is_thread,
    #         "is_pinterest": self.is_pinterest,
    #         "is_fine": self.is_fine,
            
            
    #     }

