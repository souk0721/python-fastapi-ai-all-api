import psutil

def monitor_process(file_path):
    # 실행 중인 모든 프로세스를 반복
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        # 명령줄 인자가 None인 경우 건너뛰기
        if proc.info['cmdline'] is None:
            continue

        # 프로세스의 명령줄 인자가 파일 경로를 포함하는지 확인
        if file_path in proc.info['cmdline']:
            print(f"프로세스 ID: {proc.pid}")
            print(f"프로세스 이름: {proc.name()}")
            try:
                print(f"CPU 사용량: {proc.cpu_percent()}%")
                print(f"메모리 사용량: {proc.memory_info().rss / (1024 * 1024)}MB")
            except psutil.AccessDenied:
                print("CPU 또는 메모리 정보에 접근할 수 없습니다.")
            print("-" * 40)

# 모니터링할 파일 경로
file_path = r"F:\dev\python-fastapi-ai-all-api\packages\voice_to_text_mo\voice_to_text.py"

# 모니터링 함수 호출
monitor_process(file_path)
