from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, status,File,Response
from packages.database.models import User
from packages.fastapi_mo.security_mo.security import create_access_token, verify_password,get_current_user,pwd_context
from packages.database.db import get_db,SessionLocal
from packages.fastapi_mo.schemas_mo.schema_youtube import VideoCreate
from sqlalchemy.orm import Session
from packages.utils.youtube_down import youtube_download
from packages.utils.video_converter import convert_mp4_to_hls
from packages.utils.config import VIDEO_STREAM_PATH,VIDEO_ORIGIN_STREAM_URL
from packages.database.db import create_entry
from packages.database.models import *
from packages.utils.setup_log import setup_logging
from fastapi import BackgroundTasks
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.responses import FileResponse,JSONResponse
# from packages.voice_to_text_mo.voice_to_text import process_voice_to_text
import logging
import os
from datetime import datetime
from fastapi import Request

logger = setup_logging('route_video')
router = APIRouter()

@router.post("/youtube_download")
def create_video(data: VideoCreate,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    ## 유튜브 다운로드
    result = youtube_download(data.youtube_url)
    title_video = os.path.basename(result['video_origin_path']).rsplit('.', 1)[0]
    
    # 해당 폴더가 없으면 생성
    if not os.path.exists(f'{VIDEO_STREAM_PATH}/{title_video}'):
        os.makedirs(f'{VIDEO_STREAM_PATH}/{title_video}')

    ## 파일 m38u 변환
    # m38u_file = convert_mp4_to_hls(input_file=result['video_origin_path'],output_dir=VIDEO_STREAM_PATH/title_video,title_video=title_video)
    background_tasks.add_task(convert_mp4_to_hls,input_file=result['video_origin_path'],output_dir=VIDEO_STREAM_PATH/title_video,title_video=title_video)
    data = {
        'username' : current_user.username,
        'user_id' : current_user.id,
        'youtube_url' : data.youtube_url,
        'title' : result['title'],
        'author' : result['author'],
        'video_origin_path' : result['video_origin_path'],
        'stream_url' : f'{VIDEO_ORIGIN_STREAM_URL}/{title_video}/{title_video}.m3u8',
        'save_folder_path': f'{VIDEO_STREAM_PATH}/{title_video}'
        
    }
    
    try:
        logger.info(f"username : {data['username']} / title : {data['title']} / DB SAVE start")
        obj = create_entry(
                db=db,
                model_class=YoutubeFile,
                user_id=data['user_id'],
                youtube_url=data['youtube_url'],
                title=data['title'],
                author=data['author'],
                video_origin_path=data['video_origin_path'],
                stream_url=data['stream_url'],
                save_folder_path=data['save_folder_path'],
                # whisper_json=voice_text_json,
                # is_checked=True
            )
        db.commit()
        
    except Exception as e:
        # 오류 발생 시 세션 롤백
        db.rollback()
        logger.error(e)
        # logger.error("비동기 작업 오류")
        raise e

    finally:
        # 작업 완료 후 세션 닫기
        db.close()
        logger.info(f"username : {data['username']} / title : {data['title']} / DB SAVE complete")
    
    
    
    
    ## 백그라운드에서 돌아가게하는 코드
    ## 똑같이 특정 길이기 상대적으로 긴 동영상의 경우 프로세스가 메모리때문에 종료된다,
    # background_tasks.add_task(process_voice_to_text,data)
    
    

    return data


@router.post("/voice_to_text")
def create_video(data: VideoCreate,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    pass

# @router.get("/static/{file_path:path}")
# async def get_media_url(file_path: str, current_user: User = Depends(get_current_user)):
#     # 파일 위치 확인
#     file_location = f"static/{file_path}"

#     # 파일 존재 여부 확인
#     if not os.path.exists(file_location):
#         raise HTTPException(status_code=404, detail="File not found")

#     # 외부에서 접근 가능한 URL 생성
#     # 이 예시에서는 단순히 파일 위치를 반환하고 있지만,
#     # 실제로는 외부에서 접근 가능한 URL을 생성하여 반환해야 합니다.
#     url = f"https://video.money369.co.kr/static/{file_path}"

#     return JSONResponse({"url": url})

import hmac
import hashlib
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException

SECRET_KEY = "shgustjr1!"  # 서버의 비밀 키

def generate_signed_url(file_path: str, user_id: str, expires_in: int = 3600):
    # 만료 시간 설정
    expire_at = datetime.utcnow() + timedelta(seconds=expires_in)
    expire_timestamp = int(expire_at.timestamp())

    # 서명할 원본 문자열 생성
    original_string = f"{file_path}{user_id}{expire_timestamp}"

    # HMAC을 사용하여 서명 생성
    signature = hmac.new(SECRET_KEY.encode(), original_string.encode(), hashlib.sha256).hexdigest()

    # 서명된 URL 반환
    return f"http://yourserver.com/{file_path}?user_id={user_id}&expire={expire_timestamp}&signature={signature}"

def verify_signature(file_path: str, user_id: str, expire_timestamp: int, signature: str):
    # 서명 검증
    original_string = f"{file_path}{user_id}{expire_timestamp}"
    expected_signature = hmac.new(SECRET_KEY.encode(), original_string.encode(), hashlib.sha256).hexdigest()
    return expected_signature == signature

# @router.get("/static/{file_path:path}")
# async def read_static(file_path: str):
#     file_location = f"static/{file_path}"
#     print(file_location)

#     # 파일 확장자에 따라 적절한 MIME 타입 설정
#     file_extension = os.path.splitext(file_path)[1]
#     if file_extension.lower() == ".m3u8":
#         print(file_extension)
#         media_type = "application/vnd.apple.mpegurl"
#     else:
#         media_type = None  # 기본값 사용

#     try:
#         return FileResponse(file_location, media_type=media_type)
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="File not found")
    
# @router.get("/static/{file_path:path}")
# async def read_static(file_path: str):
#     file_location = f"static/{file_path}"
#     print(file_location)

#     try:
#         file_url = f"https://video.money369.co.kr/{file_location}"
#         return JSONResponse(content={"url": file_url})
#     except FileNotFoundError:
# #         raise HTTPException(status_code=404, detail="File not found")

@router.get("/static/{file_path:path}")
async def read_static(file_path: str):
    file_location = f"static/{file_path}"
    print(file_location)

    # 파일 확장자에 따라 적절한 MIME 타입 설정
    file_extension = os.path.splitext(file_path)[1]
    if file_extension.lower() == ".m3u8":
        print(file_extension)
        media_type = "application/vnd.apple.mpegurl"
    else:
        media_type = None  # 기본값 사용

    try:
        return FileResponse(file_location, media_type=media_type)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")



