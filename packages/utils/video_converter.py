import subprocess
import os
from pathlib import Path
from moviepy.editor import VideoFileClip


## 원본의 video를 m3u8로 변환
def convert_mp4_to_hls(input_file, output_dir,title_video):
    # HLS 변환을 위한 ffmpeg 명령
    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-profile:v', 'baseline',      # 베이스라인 프로필
        '-level', '3.0',               # 레벨 3.0
        '-s', '640x360',               # 출력 해상도
        '-start_number', '0',         # 시작 번호
        '-hls_time', '10',            # 각 ts 파일당 시간(초)
        '-hls_list_size', '0',        # 플레이리스트에 저장되는 ts 파일의 최대 개수(0은 무제한)
        '-f', 'hls',                  # 출력 포맷
        '-preset', 'ultrafast',       # 빠르게
        '-crf', '28',                 # 화질 저하
        '-threads', '4',              # 쓰레드
        f'{output_dir}/{title_video}.m3u8' # 출력 m3u8 파일 경로
    ]
    subprocess.run(cmd)
    return title_video

## m3u8을 편집하고 저장        
def m3u8_edit_video(origin_video_path,output_path):
    # 영상 파일을 불러옵니다.
    clip = VideoFileClip(origin_video_path)

    # .m3u8 형식으로 저장하기 위해 ffmpeg를 사용합니다.
    # .m3u8은 실제 비디오 데이터를 포함하지 않기 때문에 .ts 파일들과 함께 생성됩니다.
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac', preset='ultrafast', write_logfile=False)
    return os.path.abspath(output_path)

def mp4_edit_video(origin_video_path, start, end, output_path):
    # 영상 파일을 불러옵니다.
    clip = VideoFileClip(origin_video_path).subclip(start, end)

    # .m3u8 형식으로 저장하기 위해 ffmpeg를 사용합니다.
    # .m3u8은 실제 비디오 데이터를 포함하지 않기 때문에 .ts 파일들과 함께 생성됩니다.
    clip.write_videofile(output_path)
    return os.path.abspath(output_path)