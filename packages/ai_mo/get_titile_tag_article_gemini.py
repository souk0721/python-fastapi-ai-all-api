from packages.database.db import *
from packages.database.models import *
from dotenv import dotenv_values
from pathlib import Path
import os,time
from langchain_google_genai import ChatGoogleGenerativeAI
from packages.utils.setup_log import setup_logging
config = dotenv_values(".env")
GOOGLE_API_KEY2 = config.get('GEMINI_API_KEY2')

lim = ChatGoogleGenerativeAI(model='gemini-pro',google_api_key=GOOGLE_API_KEY2)
db = SessionLocal()
logger = setup_logging('auto_get_titile_tag_article_gemini')

def get_title_tags_article_gemini(text):
    prompt=text +'''
    Using the text above as a guide, keep your title under 15 words,
    tags should be less than 5, and article should be more than 100 characters including your thoughts, 
    Write it in JSON format using the example below, and write the value in Korean.
    
    example:
    
    [
        {
            "title" : "",
            "tags" : ['','',''],
            "article" : ""
        }
    
    ]
    
    
    ''' 
    time.sleep(2)
    result = lim.invoke(prompt)
    
    try:
        result = json.loads(result.content)
    
    except:
        print('실패')
        print(result.content)
        # # result = lim.invoke(prompt)
        cleaned_text = result.content.replace("```", "").replace("json", "").replace("JSON", "")
        # result = json.dumps(cleaned_text)
        result = json.loads(cleaned_text)
        print('자손')
        print(result)
    
    return result

while True:
    obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,
                                    is_gemini=True,
                                    gemini_text_failed_count=0,
                                    gemini_title_tag_failed_count=0,
                                    ai_title_tag_article=None,
                                    
                                    )
    if obj:
        try:
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_titile_tag_article_gemini complete")
        
            shorts_texts = str([item['shorts'] for item in obj.gemini])
            # 각 텍스트 앞에 번호를 붙여서 출력
            prom_text = ''
            for index, text in enumerate(obj.gemini, start=1):
                prom_text = prom_text + f"{index}. {text['shorts']}" +'\n'
                
            # print(prom_text)
            result = get_title_tags_article_gemini(prom_text)
            obj.ai_title_tag_article = result
            # obj.is_gemini = True
            db.commit()
            print('완료')
            
        except Exception as e:
            # 오류 발생 시 세션 롤백
            obj.gemini_text_failed_count += 1
            db.commit()
            logger.error(e)
            raise e

        finally:
            # 작업 완료 후 세션 닫기
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_titile_tag_article_gemini complete")
            db.close()
    print('30sec wait')
    time.sleep(30)
        
    
    
    
    # ## shorts 부분만을 뺴와서 제미나이에게 title, tag, article 뽑아냄.
    # shorts_texts = [item['shorts'] for item in shorts_result]
    
    # print(shorts_texts)
    
