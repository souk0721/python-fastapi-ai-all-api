import subprocess
import os
from pathlib import Path
from dotenv import dotenv_values
config = dotenv_values(".env") ## 프로젝트 최상단 폴더의 .env 파일을 가져온다.

## 폴더 셋팅
BASE_DIR = Path(os.getcwd())
STATIC_PATH = 'static'
VIDEO_PATH = 'video'
VIDEO_ORIGIN_PATH = 'origin'
VIDEO_ORIGIN_STREAM = 'stream'
VIDEO_PROCESS_STREAM = 'edit_video'
IMG_PATH = 'img'

UPLOAD_DIR = BASE_DIR / STATIC_PATH
VIDEO_DIR = UPLOAD_DIR / VIDEO_PATH
IMG_DIR = UPLOAD_DIR / IMG_PATH


# 필요한 디렉토리 생성
for directory in [UPLOAD_DIR, VIDEO_DIR, IMG_DIR]:
    if not directory.exists():
        directory.mkdir(parents=True)
        
## 가공되지 않은 비디오 원본 파일을 저장
VIDEO_ORIGIN_PATH  = VIDEO_DIR / VIDEO_ORIGIN_PATH
## m3u8로 변환된 비디오 파일 저장
VIDEO_STREAM_PATH  = VIDEO_DIR / VIDEO_ORIGIN_STREAM
## m3u8비디오의 부분 편집을 저장
VIDEO_PROCESS_PATH  = VIDEO_DIR / VIDEO_PROCESS_STREAM


VIDEO_ORIGIN_STREAM_URL = f'{STATIC_PATH}/{VIDEO_PATH}/{VIDEO_ORIGIN_STREAM}'
EDIT_PROCESS_VIDEO_URL = f'{STATIC_PATH}/{VIDEO_PATH}/{VIDEO_PROCESS_STREAM}'

# 비디오 관련 디렉토리 생성
for directory in [VIDEO_ORIGIN_PATH, VIDEO_STREAM_PATH, VIDEO_PROCESS_PATH]:
    if not directory.exists():
        directory.mkdir(parents=True)