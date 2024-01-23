from packages.database.db import *
from packages.database.models import *
from packages.ai_mo.rag_gemini_class_text import GeminiHandler
from dotenv import dotenv_values
from pathlib import Path
import os,time
from langchain_google_genai import ChatGoogleGenerativeAI
from packages.utils.setup_log import setup_logging
from packages.ai_mo.scikit_llm import get_short_text
config = dotenv_values(".env")

db = SessionLocal()
logger = setup_logging('auto_get_shorts_text')


while True:
    obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,is_checked=True,is_gemini=False,gemini_text_failed_count=0,)
    if obj:
        try:
            if obj.whisper_json[-1]['end']:
                logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_shorts_text complete")
                # print(obj.whisper_json[-1]['end'])
                        # 초 단위 시간
                seconds = int(obj.whisper_json[-1]['end'])

                # 분 단위로 변환
                minutes = seconds / 60

                # if-elif-else 문을 사용하여 시간 분류
                # gemini = GeminiHandler(obj)
                
                # if minutes < 5:
                #     print("5분 미만")
                #     data = gemini.get_short_text(json_data=obj.whisper_json,text_count=1500)
                # elif minutes <= 10:
                #     print("10분 이하")
                #     data = gemini.get_short_text(json_data=obj.whisper_json,text_count=3000)
                # elif minutes <= 20:
                #     print("20분 이하")
                #     data = gemini.get_short_text(json_data=obj.whisper_json,text_count=6000)
                # else:
                #     print("30분 이상")
                #     data = gemini.get_short_text(json_data=obj.whisper_json,text_count=8000)
                if minutes < 5:
                    print("5분 미만")
                    data = get_short_text(json_data=obj.whisper_json,text_count=1500)
                elif minutes <= 10:
                    print("10분 이하")
                    data = get_short_text(json_data=obj.whisper_json,text_count=3000)
                elif minutes <= 20:
                    print("20분 이하")
                    data = get_short_text(json_data=obj.whisper_json,text_count=6000)
                else:
                    print("30분 이상")
                    data = get_short_text(json_data=obj.whisper_json,text_count=8000)
                print(data)
            obj.gemini = data
            obj.is_gemini = True
            # obj.gemini_text_failed_count = 0
            db.commit()
            print('완료')
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_shorts_text complete")
            
        except Exception as e:
            # 오류 발생 시 세션 롤백
            # db.delete(obj)
            if obj.gemini_text_failed_count is None:
                obj.gemini_text_failed_count = 1
            else:
                obj.gemini_text_failed_count += 1
            db.commit()
            logger.error(f"username : {obj.user.username} / title : {obj.title} / auto_get_shorts_text failed")
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
    
