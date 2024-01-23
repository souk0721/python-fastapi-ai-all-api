import os,re

def create_directory_if_not_exists(directory_path):
    """
    지정된 경로에 폴더가 없으면 생성하는 함수

    Parameters:
    - directory_path (str): 생성하려는 폴더의 경로

    Returns:
    - None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")
        
        
def safe_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)