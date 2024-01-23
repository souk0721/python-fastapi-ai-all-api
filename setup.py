from setuptools import setup, find_packages

setup(
    name='all_api', # 제목 변경
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # 'google-api-python-client==2.97.0', # 구글 API 
        # 'google-auth-httplib2==0.1.0',# 구글 API
        # 'google-auth-oauthlib==1.0.0',# 구글 API
        'librosa==0.10.1',
        'moviepy==1.0.3', # 무비 파이
        # 'oauth2client==4.1.3',
        'openai', #오폰 AI
        'opencv-contrib-python',
        'Pillow', # 이미지
        # 'pyttsx3',
        # 'webuiapi==0.9.5',#스테이블 디퓨전 API
        'notion-client==2.0.0', #노션 클라이언트 API
        'matplotlib',
        'python-dotenv', # 파이썬 환경 설정
        # 'qrcode', # QR코드 만들기
        # 'py3-pinterest==1.3.0', #Pinterest API 새로 설치하면 수정해야됨.
        # 'selenium==4.9.0', # 셀레니움
        # 'streamlit', # 스트림릿
        # 'playwright', # 웹 자동화 프로그램
        # 'bardapi', # 바드 API
		'sqlalchemy', # sqlalchemy
        'alembic', # sqlalchemy
        'fastapi',
        'psycopg2',
        'passlib',
        'bcrypt==4.0.1',
        'pytube',
        'faster-whisper', #faster-whisper
        'deepl', #deepl
        'psutil', #psutil
        'google-generativeai', #google-generativeai
        'langchain-google-genai', #langchain-google-genai
        'langchain', #langchain
        'tiktoken', #tiktoken
        'pypdf', #pypdf
        'sentence_transformers', #sentence_transformers
        'chromadb', #chromadb
        'nltk', #nltks
        ## 양자화에 필요한 라이브러리
        # 'bitsandbytes',
        'transformers',
        'peft',
        'accelerate',
        ## scikit-llm
        'scikit-llm',
        
        
        
    ],
    author='souk0721',
    author_email='souk0721@gmail.com',
    description='all_api',
    url='https://money369.co.kr',
)