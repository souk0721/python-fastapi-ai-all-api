from packages.database.db import *
from packages.database.models import *
from dotenv import dotenv_values
from pathlib import Path
import os,time
from langchain_google_genai import ChatGoogleGenerativeAI
from packages.utils.setup_log import setup_logging
config = dotenv_values(".env")
GOOGLE_API_KEY = config.get('GEMINI_API_KEY')

lim = ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=GOOGLE_API_KEY)
db = SessionLocal()
logger = setup_logging('auto_get_text_gemini')

def get_text_gemini(json_data):
    chunk_index = []
    current_paragraph = ''
    for index,item in enumerate(json_data):
        current_paragraph += str(f" {{'text' : '{item['text']}'}}")     
        current_paragraph += str(f" {{'start' : '{item['start']}'}}")     
        current_paragraph += str(f" {{'end' : '{item['end']}'}}")       
        if len(current_paragraph) > 3000:
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
    result_list =[]
    for start, end in ranges:
        data = ''
        print(f"{json_data[start]}번부터 {json_data[end]}번까지")
        for i in range(start, end + 1):
            if i < len(json_data):
                # print(json_data[i])  # 혹은 원하는 형태로 json_data[i] 처리
                data += str(json_data[i]) +'/n'
            else:
                break  # json_data의 길이를 초과하는 경우 반복문 종료
        
        prompt=str([data]) +'''
        The list above shows the start and end time of the video and the voiceover separated by text. 
        Refer to the text and summarize it into 3 or fewer lines, and make sure to write 'start' and 'end',
        Write it in JSON format using the example below, and write the value in Korean.
        
         example:
         
        [
            {
                "start" : "",
                "shorts" : "",
                "end" : ""
            },
            {
                "start" : "",
                "shorts" : "",
                "end" : ""
            },
            {
                "start" : "",
                "shorts" : "",
                "end" : ""
            },
        ]
        
        
        
        ''' 
        # prompt=str([data]) +'''
        # 위의 리스트는 동영상의 start 시간과 end 시간 그리고 음성을 text로 분리한 것이다. 
        # text를 참고하여 요약해서 3개이하로 만들어 주고, 'start'부터 'end'를 꼭 작성해 주고,
        # 아래의 예시를 참고하여 JSON 형식으로 작성해주고, value는 한국어로 작성해줘
        
        #  예시)
        # [
        #     {
        #         "start" : "",
        #         "shorts" : "",
        #         "end" : ""
        #     },
        #     {
        #         "start" : "",
        #         "shorts" : "",
        #         "end" : ""
        #     },
        #     {
        #         "start" : "",
        #         "shorts" : "",
        #         "end" : ""
        #     },
        # ]
        
        
        
        # ''' 
        time.sleep(10)
        result = lim.invoke(prompt)
        
        try:
            result = json.loads(result.content)
            print(result)
        
        except:
            # print('실패')
            # print(result.content)
            result = lim.invoke(prompt)
            # cleaned_text = result.content.replace("```", "").replace("json", "").replace("JSON", "")
            result = json.loads(result)
        
        result_list = result_list + result
    
    return result_list



while True:
    obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,is_gemini=False,is_checked=True,gemini_text_failed_count=0)
    if obj:
        try:
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_text_gemini complete")
            ## 제미나이에서 요약함.
            ## [{'start': '0.18', 'shorts': '은행지점 빠르게 문 닫음', 'end': '2.52'}, 
            # {'start': '38.2', 'shorts': 'AI, 인공지성 생활 속 활발, 은행 창구 직원 위협 받음', 'end': '42.68'}, 
            # {'start': '60.88', 'shorts': '세계 경제 포럼: 5년간 25% 직업 변화 예상', 'end': '62.98'}, 
            shorts_result = get_text_gemini(obj.whisper_json)
            obj.gemini = shorts_result
            obj.is_gemini = True
            # obj.gemini_text_failed_count = 0
            db.commit()
            print('완료')
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_text_gemini complete")
            
        except Exception as e:
            # 오류 발생 시 세션 롤백
            # db.delete(obj)
            if obj.gemini_text_failed_count is None:
                obj.gemini_text_failed_count = 1
            else:
                obj.gemini_text_failed_count += 1
            db.commit()
            logger.error(f"username : {obj.user.username} / title : {obj.title} / auto_get_text_gemini delete")
            # logger.error(e)
            raise e

        finally:
            # 작업 완료 후 세션 닫기
            
            db.close()
    print('30sec wait')
    time.sleep(30)
        
    
    
    
    # ## shorts 부분만을 뺴와서 제미나이에게 title, tag, article 뽑아냄.
    # shorts_texts = [item['shorts'] for item in shorts_result]
    
    # print(shorts_texts)
    
