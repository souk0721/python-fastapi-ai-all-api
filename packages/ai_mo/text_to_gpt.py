import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available
from packages.database.db import *
from packages.database.models import *
from faster_whisper import WhisperModel
from packages.ai_mo.openai_class import ChatGPTApi
import torch
import time


db = SessionLocal()
gpt = ChatGPTApi()
# while True:
    
    ## 첫번 째 
obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,is_gpt=False)
if obj:    
    print(obj.whisper_json)
    result = gpt.ai_shorts(str(obj.whisper_json))
    print(result)
# print('10sec wait')
    # time.sleep(10)
    