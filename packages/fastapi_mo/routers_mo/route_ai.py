from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, status,File,Response
from packages.database.models import User
from packages.fastapi_mo.security_mo.security import create_access_token, verify_password,get_current_user,pwd_context
from packages.database.db import get_db,SessionLocal
from packages.fastapi_mo.schemas_mo.schema_youtube import VideoCreate
from packages.fastapi_mo.schemas_mo.schema_ai import Ai
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
from sqlalchemy import func,text,literal,cast
from sqlalchemy.sql.expression import lateral,any_
from sqlalchemy.sql import select, literal_column
# from sqlalchemy import func, JSONB
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import aliased



logger = setup_logging('route_ai')
router = APIRouter()


@router.post("/search_text")
def ai_search(data: Ai,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    ## 유튜브 다운로드
    q = data.q
    # q = f"%{data.q}%" 
    # print(q)
        # whisper_json 필드에서 q 값을 포함하는 레코드 검색
    # whisper_json 필드에서 q 값을 포함하는 레코드 검색
    # JSON 필드에서 q 값을 포함하는 레코드 검색
    # query = db.query(YoutubeFile).filter(
    #     YoutubeFile.whisper_json.op('->')('text').cast(JSON).contains(q)
    # )

    # # 쿼리 실행 및 결과 출력
    # results = query.all()
    # for record in results:
    #     print(record)
    
    
#     query = db.query(YoutubeFile).filter(
#     YoutubeFile.whisper_json.any(
#         func.cast(YoutubeFile.whisper_json.op('->>')('text'), JSON).ilike(q)
#     )
# )
    
    
    # whisper_json 컬럼에서 'text' 키의 값이 q 변수와 일치하는 행 찾기
    # JSON 배열의 각 요소에 접근하여 'text' 키의 값이 q 변수와 일치하는 행 찾기
    # query = db.query(YoutubeFile).filter(
    #     # YoutubeFile.whisper_json.op('->')(0).cast(JSON).op('->>')('text').contains(q)
    #     YoutubeFile.whisper_json.op('->')(0).cast(JSON).op('->>')('text').ilike(q)
    # )
    
    # JSON 배열의 각 요소를 개별 행으로 만들고 'text' 키의 값이 q 변수를 포함하는 행 찾기
    # query = db.query(YoutubeFile).join(
    #     lateral(func.jsonb_array_elements(YoutubeFile.whisper_json).alias('elements')),
    #     isouter=True
    # ).filter(
    #     func.jsonb_extract_path_text('elements', 'text').ilike(q)
    # )
        
        # JSON 배열의 각 요소에 접근하여 'text' 키의 값이 q 변수를 포함하는 행 찾기
    # query = db.query(YoutubeFile).filter(
    #     YoutubeFile.whisper_json.op('->')(0).cast(JSONB).op('->>')('text').ilike(f'%{q}%')
    #     # func.cast(YoutubeFile.whisper_json.op('->>')('text'), JSONB).ilike(q)
    # )
        # Create an aliased expression for the JSON array elements
    # Assuming 'q' is the search string
    # 쿼리 문자열 'q'가 주어졌다고 가정합니다.
    # query = db.query(YoutubeFile).filter(
    #     any_(YoutubeFile.whisper_json.cast(JSONB).op('->>')('text').ilike(f'%{q}%'))
    # )
    # query = db.query(YoutubeFile).filter(
    #     YoutubeFile.whisper_json.cast(JSONB).contains(
    #         [{"text": q}]
    #     )
    # )
    # query = db.query(YoutubeFile).filter(
        
    #         func.cast(YoutubeFile.whisper_json.op('->>')('text'), JSON).ilike(q)
        
    # )
    #     # Assuming 'q' is the search string
    # query = db.query(YoutubeFile).filter(
    #     func.jsonb_array_elements(YoutubeFile.whisper_json.cast(JSONB)).op('->>')('text').ilike(f'%{q}%')
    # )
    
        # JSONB 형식으로 필드가 설정되어 있는지 확인하세요.
    # 쿼리
    with SessionLocal() as session:
        sql_query = text("""
            SELECT *
            FROM youtube_file
            WHERE EXISTS (
                SELECT 1
                FROM jsonb_array_elements(whisper_json) as elem
                WHERE elem ->> 'text' LIKE :q
            )
        """)
        result = session.execute(sql_query, {'q': f'%{q}%'}).fetchall()
        # print(result)
    search_arry=[]
    for res in result:
        
        whisper_json = res.whisper_json
        
        for entry in whisper_json:
            search_json = {}
            search_json['stream_url'] =res.stream_url
            if q in entry['text']:
                start = entry.get('start')
                end = entry.get('end')
                print(f"Text: {entry['text']}, Start: {start}, End: {end}")
                search_json['text'] =entry['text']
                search_json['start'] =entry.get('start')
                search_json['end'] =entry.get('end')
                search_arry.append(search_json)
    print(search_arry)
    # query = db.query(YoutubeFile).filter(
    # func.jsonb_array_elements(YoutubeFile.whisper_json.cast(JSONB)).op('->>')('text').ilike(f"%{q}%")
    # )
    
    # # 서브쿼리 생성
    # subq = select([
    #     func.jsonb_array_elements(YoutubeFile.whisper_json.cast(JSONB)).op('->>')('text').label('text')
    # ]).alias('subq')

    # # 메인 쿼리에서 서브쿼리와 조인
    # query = db.query(YoutubeFile).join(
    #     subq, YoutubeFile.whisper_json.op('->>')('text') == subq.c.text
    # ).filter(
    #     subq.c.text.ilike(f"%{q}%")
    # )
        # 서브쿼리 생성
    # subq = select([
    #     func.jsonb_array_elements(YoutubeFile.whisper_json.cast(JSONB)).op('->>')('text').label('text')
    # ]).subquery()

    # # 메인 쿼리에서 서브쿼리와 조인
    # query = db.query(YoutubeFile).join(
    #     subq, YoutubeFile.whisper_json.op('->>')('text') == subq.c.text
    # ).filter(
    #     subq.c.text.ilike(f"%{q}%")
    # )

    
    # query = db.query(YoutubeFile).filter(
    #     text("whisper_json -> 'text' ilike :q")
    # ).params(q=f"%{q}%")
    #  # 결과 출력
    # for youtube_file in query:
    #     print(youtube_file.stream_url)
    
    #     # JSON 배열의 모든 요소에서 q 값을 포함하는 레코드 검색
    # query = db.query(YoutubeFile).filter(
    #     YoutubeFile.whisper_json.op('->')('text').cast(String).contains(q)
    # )
    #     # 쿼리 실행 및 결과 출력
    # results = query.all()
    # for record in results:
    #     print(record)
    
    # YouTubeFile의 모든 행과 whisper_json의 각 요소를 조인하고, 'text' 키의 값이 q를 포함하는 행을 필터링
    # query = db.query(YoutubeFile).join(
    #     select([
    #         literal_column("'elements'").label('key'),
    #         func.jsonb_array_elements(YoutubeFile.whisper_json).label('value')
    #     ]).lateral(),
    #     isouter=True
    # ).filter(
    #     func.jsonb_extract_path_text(literal_column('value'), literal_column('text')).ilike(q)
    # )
    
    # result = db.query(YoutubeFile).filter(
    #     YoutubeFile.whisper_json.any({"text": q})
    # ).all()

    # for item in result:
    #     print(item.id, item.whisper_json)
    
    # result = db.query(YoutubeFile).filter(
    #     func.jsonb_each_text(YoutubeFile.whisper_json).contains({'value': q})
    # ).all()

    # for item in result:
    #     print(item.id, item.whisper_json)
    
    # 세션 생성 및 raw SQL 쿼리 실행
    # with SessionLocal() as session:
    #     sql_query = text("""
    #         SELECT * FROM youtube_file
    #         WHERE whisper_json::jsonb @> ANY (ARRAY [jsonb_build_object('text', :q)])
    #     """)
    #     result = session.execute(sql_query, {'q': q}).fetchall()

    #     for item in result:
    #         print(item)
    

   
    
    # result = youtube_download(data.youtube_url)
    # title_video = os.path.basename(result['video_origin_path']).rsplit('.', 1)[0]
    
    # # 해당 폴더가 없으면 생성
    # if not os.path.exists(f'{VIDEO_STREAM_PATH}/{title_video}'):
    #     os.makedirs(f'{VIDEO_STREAM_PATH}/{title_video}')

    # ## 파일 m38u 변환
    # # m38u_file = convert_mp4_to_hls(input_file=result['video_origin_path'],output_dir=VIDEO_STREAM_PATH/title_video,title_video=title_video)
    # background_tasks.add_task(convert_mp4_to_hls,input_file=result['video_origin_path'],output_dir=VIDEO_STREAM_PATH/title_video,title_video=title_video)
    # data = {
    #     'username' : current_user.username,
    #     'user_id' : current_user.id,
    #     'youtube_url' : data.youtube_url,
    #     'title' : result['title'],
    #     'author' : result['author'],
    #     'video_origin_path' : result['video_origin_path'],
    #     'stream_url' : f'{VIDEO_ORIGIN_STREAM_URL}/{title_video}/{title_video}.m3u8',
    #     'save_folder_path': f'{VIDEO_STREAM_PATH}/{title_video}'
        
    # }
    
    # try:
    #     logger.info(f"username : {data['username']} / title : {data['title']} / DB SAVE start")
    #     obj = create_entry(
    #             db=db,
    #             model_class=YoutubeFile,
    #             user_id=data['user_id'],
    #             youtube_url=data['youtube_url'],
    #             title=data['title'],
    #             author=data['author'],
    #             video_origin_path=data['video_origin_path'],
    #             stream_url=data['stream_url'],
    #             save_folder_path=data['save_folder_path'],
    #             # whisper_json=voice_text_json,
    #             # is_checked=True
    #         )
    #     db.commit()
        
    # except Exception as e:
    #     # 오류 발생 시 세션 롤백
    #     db.rollback()
    #     logger.error(e)
    #     # logger.error("비동기 작업 오류")
    #     raise e

    # finally:
    #     # 작업 완료 후 세션 닫기
    #     db.close()
    #     logger.info(f"username : {data['username']} / title : {data['title']} / DB SAVE complete")
    
    
    
    
    ## 백그라운드에서 돌아가게하는 코드
    ## 똑같이 특정 길이기 상대적으로 긴 동영상의 경우 프로세스가 메모리때문에 종료된다,
    # background_tasks.add_task(process_voice_to_text,data)
    
    

    return data


# @router.post("/voice_to_text")
# def create_video(data: VideoCreate,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
# ):
#     pass

# # @router.get("/static/{file_path:path}")
# # async def get_media_url(file_path: str, current_user: User = Depends(get_current_user)):
# #     # 파일 위치 확인
# #     file_location = f"static/{file_path}"

# #     # 파일 존재 여부 확인
# #     if not os.path.exists(file_location):
# #         raise HTTPException(status_code=404, detail="File not found")

# #     # 외부에서 접근 가능한 URL 생성
# #     # 이 예시에서는 단순히 파일 위치를 반환하고 있지만,
# #     # 실제로는 외부에서 접근 가능한 URL을 생성하여 반환해야 합니다.
# #     url = f"https://video.money369.co.kr/static/{file_path}"

# #     return JSONResponse({"url": url})

# import hmac
# import hashlib
# from datetime import datetime, timedelta
# from fastapi import FastAPI, HTTPException

# SECRET_KEY = "shgustjr1!"  # 서버의 비밀 키

# def generate_signed_url(file_path: str, user_id: str, expires_in: int = 3600):
#     # 만료 시간 설정
#     expire_at = datetime.utcnow() + timedelta(seconds=expires_in)
#     expire_timestamp = int(expire_at.timestamp())

#     # 서명할 원본 문자열 생성
#     original_string = f"{file_path}{user_id}{expire_timestamp}"

#     # HMAC을 사용하여 서명 생성
#     signature = hmac.new(SECRET_KEY.encode(), original_string.encode(), hashlib.sha256).hexdigest()

#     # 서명된 URL 반환
#     return f"http://yourserver.com/{file_path}?user_id={user_id}&expire={expire_timestamp}&signature={signature}"

# def verify_signature(file_path: str, user_id: str, expire_timestamp: int, signature: str):
#     # 서명 검증
#     original_string = f"{file_path}{user_id}{expire_timestamp}"
#     expected_signature = hmac.new(SECRET_KEY.encode(), original_string.encode(), hashlib.sha256).hexdigest()
#     return expected_signature == signature

# # @router.get("/static/{file_path:path}")
# # async def read_static(file_path: str):
# #     file_location = f"static/{file_path}"
# #     print(file_location)

# #     # 파일 확장자에 따라 적절한 MIME 타입 설정
# #     file_extension = os.path.splitext(file_path)[1]
# #     if file_extension.lower() == ".m3u8":
# #         print(file_extension)
# #         media_type = "application/vnd.apple.mpegurl"
# #     else:
# #         media_type = None  # 기본값 사용

# #     try:
# #         return FileResponse(file_location, media_type=media_type)
# #     except FileNotFoundError:
# #         raise HTTPException(status_code=404, detail="File not found")
    
# # @router.get("/static/{file_path:path}")
# # async def read_static(file_path: str):
# #     file_location = f"static/{file_path}"
# #     print(file_location)

# #     try:
# #         file_url = f"https://video.money369.co.kr/{file_location}"
# #         return JSONResponse(content={"url": file_url})
# #     except FileNotFoundError:
# # #         raise HTTPException(status_code=404, detail="File not found")

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



