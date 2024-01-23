from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from packages.database.models import *
from sqlalchemy.orm import Session
from sqlalchemy import desc
from dotenv import dotenv_values
import os
# 예: 사용자의 홈 디렉토리에 데이터베이스 파일을 두는 경우
# 현재 작업 디렉토리의 경로를 구함
# current_directory = os.getcwd()
config = dotenv_values(".env")
DATABASE_URL = config.get('DATABASE_URL')   
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 데이터베이스 세션을 가져오는 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

######
def create_entry(db: Session, model_class, **kwargs):
    new_entry = model_class(**kwargs)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_entry(db: Session, model_class, entry_id: int):
    return db.query(model_class).filter(model_class.id == entry_id).first()

def get_all_entries_limit(db: Session, model_class, skip: int = 0, limit: int = 15,**kwargs):
# 먼저 기본 쿼리를 생성
    query = db.query(model_class).order_by(desc(model_class.id))

    # kwargs를 사용하여 필터링 적용
    for key, value in kwargs.items():
        column = getattr(model_class, key, None)
        if column is not None:
            query = query.filter(column == value)

    # skip과 limit 적용하여 결과를 가져옴
    entry = query.offset(skip).limit(limit).all()

    return entry

def get_all_entries_limit_one(db: Session, model_class, **kwargs):
    query = db.query(model_class).order_by(desc(model_class.id))
    for key, value in kwargs.items():
        column = getattr(model_class, key, None)
        if column is not None:
            query = query.filter(column == value)
    entry = query.first()
    return entry


def get_all_entries(db: Session, model_class, skip: int = 0,**kwargs):
    query = db.query(model_class).order_by(desc(model_class.id))
    for key, value in kwargs.items():
        column = getattr(model_class, key, None)
        if column is not None:
            query = query.filter(column == value)
    entry = query.offset(skip).all()
    return entry
    

def update_entry(db: Session, model_class, entry_id: int, **kwargs):
    entry = db.query(model_class).filter(model_class.id == entry_id).first()
    if entry:
        for key, value in kwargs.items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    return None

def delete_entry(db: Session, model_class, entry_id: int):
    entry = db.query(model_class).filter(model_class.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
        return True
    return False

