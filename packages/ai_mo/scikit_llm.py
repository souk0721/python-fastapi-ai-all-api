import pathlib
import textwrap
import google.generativeai as genai
from packages.database.db import *
from packages.database.models import *
from packages.ai_mo.rag_gemini_class_text import GeminiHandler 
from dotenv import dotenv_values
from pathlib import Path
import requests
from datetime import datetime
import os,time
from langchain_google_genai import ChatGoogleGenerativeAI
import deepl

config = dotenv_values(".env")
db = SessionLocal()

OPENAI_API_KEY = config.get('OPENAI_API_KEY')
OPENAI_ORG_KEY = config.get('OPENAI_ORG_KEY')
DEEPL_API_KEY = config.get('DEEPL_API_KEY')
translator = deepl.Translator(DEEPL_API_KEY)

from skllm.config import SKLLMConfig
SKLLMConfig.set_openai_key(OPENAI_API_KEY)
SKLLMConfig.set_openai_org(OPENAI_ORG_KEY)

def summerize(data):
    from skllm.models.gpt.text2text.summarization import GPTSummarizer
    # from skllm.datasets import get_summarization_dataset
    
    X = data
    # print(X[0])
    summerize = GPTSummarizer(model="gpt-3.5-turbo", max_words=15)
    X_summarized = summerize.fit_transform(X)
    # print(X_summarized[0])
    # for i in X_summarized:
    #     print(f"요약문 : {i}")
    return X_summarized[0]

def get_short_text(json_data,text_count):
    chunk_index = []
    current_paragraph = ''
    for index,item in enumerate(json_data):
        current_paragraph += str(f" {{'text' : '{item['text']}'}}")     
        current_paragraph += str(f" {{'start' : '{item['start']}'}}")     
        current_paragraph += str(f" {{'end' : '{item['end']}'}}")       
        if len(current_paragraph) > text_count:
            chunk_index.append(index)
            # print('index : ' + str(index))
            # print(current_paragraph)
            current_paragraph=''
    
    
    
     # 마지막 남은 데이터 처리
    if current_paragraph:
        chunk_index.append(len(json_data) - 1)
        print('index : ' + str(len(json_data) - 1))
        # print(current_paragraph)
    print(chunk_index)
    
    ranges = []

    # 첫 번째 구간의 시작점은 0
    start = 0

    for end in chunk_index:
        # 각 구간은 start부터 end까지 (end는 포함하지 않음)
        ranges.append((start, end))

        # 다음 구간의 시작점은 현재 구간의 끝점 + 1
        start = end + 1

    # 결과 출력
    # complete_result = []
    result_list =[]
    for start, end in ranges:
        result_json = {}
        print(json_data[start]['start'])
        print(json_data[end]['end'])
        result_json['start'] = json_data[start]['start']
        result_json['end'] = json_data[end]['end']
        data = ""
        print(f"{json_data[start]}번부터 {json_data[end]}번까지")
        for i in range(start, end + 1):
            if i < len(json_data):
                # print(json_data[i])  # 혹은 원하는 형태로 json_data[i] 처리
                data += str(json_data[i]['text'])
            else:
                break  # json_data의 길이를 초과하는 경우 반복문 종료
        ## GPT 사용
        # result_json['shorts_eng'] = summerize([data])
        ## Gemini 사용
        result_json['shorts_eng'] = summerize([data])
        time.sleep(1)
        ## deepl로 변역
        kr_translate = translator.translate_text(result_json['shorts_eng'], target_lang="KO")
        result_json['shorts_kor'] = kr_translate.text
        # print(result.text)  # "Bonjour, le monde !"
        result_list.append(result_json)
        
        
    
    return result_list



def first():
    from skllm.models.gpt.classification.zero_shot import ZeroShotGPTClassifier
    import pandas as pd
    
    reviews = [
        "이 영화는 정말 기쁘게 만들었다. 밝고 경쾌한 스토리와 멋진 연기가 돋보인다.",
        "엄청난 반전에 놀랐다. 예상치 못한 결말이 인상적이었다.",
        "이 영화의 공포 분위기기가 너무 무서워서 잠을 설쳤다.",
        "영화의 연출과 스토리가 너무 화가 날 정도로 실망 스러웠다.",
        "이 영화는 정말 유쾌하고 웃음이 넘쳤다. 즐거운 시간이었다.",
    ]
    clf = ZeroShotGPTClassifier()
    clf.fit(None,["기쁨","놀람","무서움","감동","화남","유쾌"])
    labels = clf.predict(reviews)
    result = pd.DataFrame({"리뷰":reviews,"감성":labels})
    print(result) 
    
def second():
    from skllm.models.gpt.classification.zero_shot import MultiLabelZeroShotGPTClassifier
    import pandas as pd
    
    mixed_emotion_revicews = [
        "이 영화는 기쁘면서도 동시에 놀라운 장면이 많았고, 감동적인 결말을 맞이했다.",
        "공포스러운 분위기 속에서도 유쾌한 요소가 있었으며, 놀라운 반전도 있었다.",
        "영화가 너무 무서워서 긴장했지만, 감동적인 메시지가 있어서 기뻤다.",
        "놀라운 시각 효과와 긴박한 기쁨을 주었지만, 무서운 장면들이 많아서 불편했다.",
        "슬픈 장면이 많아 감동적이었지만, 유쾌한 캐릭터들이 기쁨을 주었다.",
    ]
    emotion_labels = ["긍정","부정","싫음","추천"]
    clf = MultiLabelZeroShotGPTClassifier(model="gpt-3.5-turbo", max_labels=3)
    clf.fit(None,[emotion_labels])
    labels = clf.predict(mixed_emotion_revicews)
    result = pd.DataFrame({"리뷰":mixed_emotion_revicews,"감성":labels})
    print(result)

def get_title_tags(text_list):
    from skllm.models.gpt.classification.zero_shot import MultiLabelZeroShotGPTClassifier
    import pandas as pd
    
    # mixed_emotion_revicews = [
    #     "이 영화는 기쁘면서도 동시에 놀라운 장면이 많았고, 감동적인 결말을 맞이했다.",
    #     "공포스러운 분위기 속에서도 유쾌한 요소가 있었으며, 놀라운 반전도 있었다.",
    #     "영화가 너무 무서워서 긴장했지만, 감동적인 메시지가 있어서 기뻤다.",
    #     "놀라운 시각 효과와 긴박한 기쁨을 주었지만, 무서운 장면들이 많아서 불편했다.",
    #     "슬픈 장면이 많아 감동적이었지만, 유쾌한 캐릭터들이 기쁨을 주었다.",
    # ]
    emotion_labels = ["AI","인물","사회","경제","부업","ChatGPT","리뷰","사회","상품리뷰","테크"]
    clf = MultiLabelZeroShotGPTClassifier(model="gpt-3.5-turbo", max_labels=3)
    clf.fit(None,[emotion_labels])
    labels = clf.predict(text_list)
    # result = pd.DataFrame({"리뷰":text_list,"감성":labels})
    # print(result)
    return labels

# def summerize(data):
#     from skllm.models.gpt.text2text.summarization import GPTSummarizer
#     from skllm.datasets import get_summarization_dataset
    
#     X = data
#     # print(X[0])
#     summerize = GPTSummarizer(model="gpt-4", max_words=30)
#     X_summarized = summerize.fit_transform(X)
#     # print(X_summarized[0])
#     for i in X_summarized:
#         print(f"요약문 : {i}")
    
#     # for i in data:
#     #     print(f"원문: {[i]}")
#     #     print("\n")
#     #     print(f"요약문 : {X_summarized[i]}")
#     #     print("-"*50)

# # first()
# # second()
# # summerize()


###### test
# obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,is_gemini=False,is_checked=True)
# # print(obj)
# if obj:
#     if obj.whisper_json[-1]['end']:
#         # print(obj.whisper_json[-1]['end'])
#                 # 초 단위 시간
#         seconds = int(obj.whisper_json[-1]['end'])

#         # 분 단위로 변환
#         minutes = seconds / 60

#         # if-elif-else 문을 사용하여 시간 분류
#         if minutes < 5:
#             print("5분 미만")
#             data = get_text_gemini(json_data=obj.whisper_json,text_count=1500)
#         elif minutes <= 10:
#             print("10분 이하")
#             data = get_text_gemini(json_data=obj.whisper_json,text_count=3000)
#         elif minutes <= 20:
#             print("20분 이하")
#             data = get_text_gemini(json_data=obj.whisper_json,text_count=6000)
#         else:
#             print("30분 이상")
#             data = get_text_gemini(json_data=obj.whisper_json,text_count=8000)
#         print(data)
    
#     # data = get_text_gemini(obj.whisper_json)
#     # print(data)
# # summerize(data)