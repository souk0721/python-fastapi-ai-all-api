import os

# 프로젝트 루트 디렉토리 내의 폴더와 서브폴더 목록
folders = [
    "packages",
    "packages/database",
    "packages/process",
    # "my_package/flask", # flask 프로젝트 시 
    "packages/streamlit", # streamlit 프로젝트 시 
    "tests"
]

# 프로젝트 루트 디렉토리를 기준으로 각 폴더에 대해 생성
for folder in folders:
    os.makedirs(os.path.join(folder), exist_ok=True)

# 프로젝트 루트 디렉토리 내의 필요한 파일 목록
files = [
    "packages/__init__.py",
    "packages/database/__init__.py",
    "packages/database/db.py",
    "packages/database/models.py",
    "packages/process/__init__.py",
    "packages/process/process_main.py",
    "packages/streamlit/__init__.py",
    # "packages/streamlit/streamlit_main.py",
    # "tests/test_module1.py",
    # "tests/test_module2.py",
    "setup.py",
    "requirements.txt"
]

# 프로젝트 루트 디렉토리를 기준으로 각 파일에 대해 생성
for file in files:
    with open(os.path.join(file), 'w') as f:
        pass  # 파일을 생성하고 아무 내용도 작성하지 않음

print("프로젝트 루트 디렉토리 내의 폴더 구조와 파일이 생성되었습니다.")