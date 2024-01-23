from packages.database.db import *
from packages.database.models import *
from faster_whisper import WhisperModel
import torch
import time
import logging
from datetime import datetime
from packages.utils.setup_log import setup_logging

logger = setup_logging('voice_to_text')

db=SessionLocal()

## 

# def back_process_voice_to_text(data):
#     try:
#         logger.info(f"username : {data['username']} / title : {data['title']} / voice_to_text start")
#         with torch.inference_mode():
#             # (여기에 나머지 처리 코드 작성)
#             voice_text_json =[]
#             # model_size = "medium"
#             # model_size = "large-v3"
#             model_size = "base"
#             # model_size = "large-v2"
#             model = WhisperModel(model_size,device='cuda',compute_type="float16") ## GPU
#             # model = WhisperModel(model_size,device='cuda',compute_type="int8_float16") ## GPU
#             # model = WhisperModel(model_size,device='cpu',compute_type="int8") ## GPU
#             start_time = time.time()
#             # segments,info = model.transcribe(file_path,language='ko',beam_size=5)
#             segments, info = model.transcribe(data['video_origin_path'],vad_filter=True,vad_parameters=dict(min_silence_duration_ms=2000))
#             # result = segments
#             # self.voice_text = (result['text'])
#             # self.voice_text = segments
#             for i in segments:
#                 json_data ={}
#                 json_data['text'] = i.text
#                 json_data['start'] = i.start
#                 json_data['end'] = i.end
#                 voice_text_json.append(json_data)
#             # print(self.voice_text)
#             end_time = time.time()
#             elapsed_time = end_time - start_time
#             print(f"코드 실행 시간: {elapsed_time}초")
#             print(voice_text_json)
#             print('ok')
#             obj = create_entry(
#                 db=db,
#                 model_class=YoutubeFile,
#                 user_id=data['user_id'],
#                 youtube_url=data['youtube_url'],
#                 title=data['title'],
#                 author=data['author'],
#                 video_origin_path=data['video_origin_path'],
#                 stream_url=data['stream_url'],
#                 save_folder_path=data['save_folder_path'],
#                 whisper_json=voice_text_json,
#                 is_checked=True
#             )
#             db.commit()
#             print('완료')
        



#     except Exception as e:
#         # 오류 발생 시 세션 롤백
#         db.rollback()
#         logger.error(e)
#         raise e

#     finally:
#         # 작업 완료 후 세션 닫기
#         db.close()
#         logger.info(f"username : {data['username']} / title : {data['title']} / voice_to_text complete")
        
def process_voice_to_text(file_path,obj):
    try:
        logger.info(f"username : {obj.user.username} / title : {obj.title} / voice_to_text start")
        with torch.inference_mode():
            # (여기에 나머지 처리 코드 작성)
            voice_text_json =[]
            # model_size = "medium"
            model_size = "large-v3"
            # model_size = "medium"
            # model_size = "large-v2"
            model = WhisperModel(model_size,device='cuda',compute_type="float16") ## GPU
            # model = WhisperModel(model_size,device='cuda',compute_type="int8_float16") ## GPU
            # model = WhisperModel(model_size,device='cpu',compute_type="int8") ## GPU
            start_time = time.time()
            # segments,info = model.transcribe(file_path,language='ko',beam_size=5)
            segments, info = model.transcribe(file_path,vad_filter=True,vad_parameters=dict(min_silence_duration_ms=2000))
            # result = segments
            # self.voice_text = (result['text'])
            # self.voice_text = segments
            for i in segments:
                json_data ={}
                json_data['text'] = i.text
                json_data['start'] = i.start
                json_data['end'] = i.end
                voice_text_json.append(json_data)
            # print(self.voice_text)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"코드 실행 시간: {elapsed_time}초")
            print(voice_text_json)
            print('ok')
            obj.whisper_json = voice_text_json
            obj.is_checked = True

            db.commit()
            print('완료')
        

    except Exception as e:
        # 오류 발생 시 세션 롤백
        db.rollback()
        logger.error(e)
        raise e

    finally:
        # 작업 완료 후 세션 닫기
        logger.info(f"username : {obj.user.username} / title : {obj.title} / voice_to_text complete")
        db.close()
        
    

while True:
    
    ## 첫번 째 
    obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,is_checked=False)
    if obj:    
        print(obj.video_origin_path)
        process_voice_to_text(obj.video_origin_path,obj)
    print('10sec wait')
    time.sleep(10)
    