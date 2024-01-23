import pytube
import os
from packages.utils.config import VIDEO_ORIGIN_PATH
from packages.utils.create_folder import create_directory_if_not_exists,safe_filename

def youtube_download(youtube_url):
    # with torch.inference_mode():
    yt = pytube.YouTube(youtube_url)
    ys = yt.streams.get_highest_resolution()
    file_path = ys.download(VIDEO_ORIGIN_PATH)
    author = yt.author
    title = yt.title
    print(file_path)
    data = {
        'title' : title,
        'video_origin_path' : file_path,
        'author' : author
    }
    return data