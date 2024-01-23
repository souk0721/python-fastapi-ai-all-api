import pathlib
import textwrap
import google.generativeai as genai
from packages.database.db import *
from packages.database.models import *
from dotenv import dotenv_values
from pathlib import Path
import requests
from datetime import datetime
# from packages.utils.nltk_token_count import tokenize_and_check

# from package.process.utils import create_final_destination_path
# from package.elevenlabs_api.elevenlabs_create_voice import generate_and_play_audio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
config = dotenv_values(".env")
GOOGLE_API_KEY = config.get('GEMINI_API_KEY')

lim = ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=GOOGLE_API_KEY)
# result = lim.invoke('네이버에 대해 보고서를 작성해줘')

# print(result)


db = SessionLocal()



def get_text(json_data):
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
        위의 리스트는 동영상의 start 시간과 end 시간 그리고 음성을 text로 분리한 것이다. 
        text를 참고하여 요약해서 3개이하로 만들어 주고, 'start'부터 'end'를 꼭 작성해 주고,
        아래의 예시를 참고하여 JSON 형식으로 작성한다.
        
         예시)
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
        # prompt=data +'''
        # 위의 리스트는 동영상의 start 시간과 end 시간 그리고 음성을 text로 분리한 것이다. 
        # 1. start, end를 참고하여 문맥에 맞는 text를 함께 요약한다.
        # 2. 요약한 text의 'start'부터 'end'를 파악한다.
        # 3. 아래의 예시를 참고하여 JSON 형식으로 작성해줘 작성을 잘하면 팁을 2000$줄께
        #  예시)
        # [
        #     {
        #         "start" : "",
        #         "shorts" : "",
        #         "end" : ""
        #     }
        # ]
        
        
        
        # ''' 
        result = lim.invoke(prompt)
        try:
            result = json.loads(result.content)
        except:
            print('실패')
            print(result.content)
            # result = lim.invoke(prompt)
            cleaned_text = result.content.replace("```", "")
            result = json.dumps(cleaned_text)
        # result = result.content
        
        result_list = result_list + result
    
    return result_list
        
        # print(result)
        
        # print()
        
        

        # print()  # 구간 사이에 공백 줄 추가
        
        # 함수 호출 및 결과 출력
        # result = tokenize_and_check(json_data)
        
        
        
        # print(result)
        # prompt='''
        # 아래의 리스트는 동영상의 start 시간과 end 시간 그리고 text가 있다. 
        # 1. start, end를 전체의 5분의1로 나누어 해당하는 text를 요약한다.
        # 2. 요약한 text의 'start'부터 'end'를 파악한다.
        # 3. 아래의 예시를 참고하여 JSON 형식으로 작성햊줘
        #  예시)
        #     {
        #         "data"  : [
        #             {
        #                 "start" : "",
        #                 "shorts" : "",
        #                 "end" : ""
        #             },
        #             {
        #                 "start" : "",
        #                 "shorts" : "",
        #                 "end" : ""
        #             },
                    
        #         ]
        #     }
        
        
        # 아래의 글 /n
        # ''' + str(obj.whisper_json)
        
        
        # sentences = text
        # paragraph = []
        # current_paragraph = ''
        # for sentence in sentences:
        #     result_json = {}
        #     current_paragraph += sentence 
        #     # print("current_paragraph : " + current_paragraph)
        #     # 문단의 길이가 1000자를 초과하면 새로운 문단으로 생성
        #     if len(current_paragraph) > 1000:
                
        #         print("current_paragraph : " + current_paragraph)
        #         prompt = prompt + current_paragraph
        #         completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
        #                                         # 보낼 메세지 목록
        #                                         messages=[{"role": "system", "content":"넌 전문적인 소설가이다."},
        #                                                 {"role": "user", "content": prompt}]) # 사용자
                
        #         result = completion.choices[0].message.content
        #         # result = json.dumps(result)
        #         result = json.loads(result)
        #         # print(result)
            
        #         # print(result['title'])
        #         # print(result['content'])
        #         # # time.sleep(30)
                    
        #         # content = notion_ai.summarize(context=current_paragraph)
        #         # print("content : " + content)
        #         # time.sleep(30)
                
        #         # # 현재 문단을 문단 리스트에 추가
        #         result_json['title']= result['title']
        #         result_json['content'] = result['content']
        #         paragraph.append(result_json)
                
        #         # 새로운 문단을 시작
        #         current_paragraph = ''
        #         # time.sleep(5)
        # # print(current_paragraph)
        # if current_paragraph:
        #     prompt = prompt + current_paragraph
        #     completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
        #                                             # 보낼 메세지 목록
        #                                         messages=[{"role": "system", "content":"넌 전문적인 소설가이다."},
        #                                                 {"role": "user", "content": prompt}]) # 사용자
                
        #     result = completion.choices[0].message.content
        #     # result = json.dumps(result)
        #     result = json.loads(result)
        #     # print(result)
            
        #     # print(result['title'])
        #     # print(result['content'])
        #     # # time.sleep(30)
                    
        #     # content = notion_ai.summarize(context=current_paragraph)
        #     # print("content : " + content)
        #     # time.sleep(30)
            
        #     # # 현재 문단을 문단 리스트에 추가
        #     result_json['title']= result['title']
        #     result_json['content'] = result['content']
        #     paragraph.append(result_json)
        # return result_json


    
    ## 첫번 째
    


def get_title_tag(json_data):
    
    for index,data in enumerate(json_data):
        
    
        pass
   
    
     
obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,is_gpt=False)
if obj:
    # prompt='''
    #     아래의 리스트는 동영상의 start 시간과 end 시간 그리고 text가 있다. 
    #     1. 주어진 리스트의 전체 'text'를 참고하여 title을 작성한다. title은 50자 미만으로 작성한다.
    #     2. 주어진 리스트의 전체 'text'를 참고하여 tag를 작성한다. tag는 5개 이하로 한다.
    #         ex) tag =['ai','정치','사회','경제','상품리뷰','재미있는 이야기','애니리뷰','영화리뷰'] 
    #     3. 주어진 리스트의 전체 'text'를 참고하여 길게 내용을 정리해줘
    #     4. 무조건 JSON 형식으로 작성한다. 예를 들어
    #     {
    #             'title' : '전체 내용의 title'
    #             'tag' : ['ai','교육','정치','사회']
    #             'shorts'  :'이야기는 ~'
    #     }
        
    #     아래의 글 /n
    #     ''' + str(obj.whisper_json)
    title_prompt='''
        아래의 리스트는 동영상의 start 시간과 end 시간 그리고 text가 있다. 
        1. 주어진 리스트의 전체 'text'를 참고하여 title을 작성한다. title은 50자 미만으로 작성한다.
        2. 주어진 리스트의 전체 'text'를 참고하여 tag를 작성한다. tag는 5개 이하로 한다.
            ex) tag =['ai','정치','사회','경제','상품리뷰','재미있는 이야기','애니리뷰','영화리뷰'] 
        예시)
            {
                "title" : "",
                "tag" : ['', '', ''],
            }
        
        
        아래의 글 /n
        ''' + str(obj.whisper_json)
    
        
    # print(obj.whisper_json)
    # result = lim.invoke(title_prompt)
    # print(result.content)
    
    result = get_text(obj.whisper_json)
    print(result)
    
