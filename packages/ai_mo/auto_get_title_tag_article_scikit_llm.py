from packages.database.db import *
from packages.database.models import *
from packages.ai_mo.rag_gemini_class_text import GeminiHandler
from dotenv import dotenv_values
from pathlib import Path
import os,time
from langchain_google_genai import ChatGoogleGenerativeAI
from packages.utils.setup_log import setup_logging
from packages.ai_mo.scikit_llm import get_short_text,get_title_tags
config = dotenv_values(".env")

db = SessionLocal()
logger = setup_logging('auto_get_title_tag_article_scikit_llm')


while True:
    obj = get_all_entries_limit_one(db=db,model_class=YoutubeFile,
                                    is_gemini=True,
                                    gemini_text_failed_count=0,
                                    gemini_title_tag_failed_count=0,
                                    ai_title_tag_article=None,
                                    )
    if obj:
        try:
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_title_tag_article_scikit_llm complete")
            # shorts_texts = ''
            # for item in obj.gemini:
                
            #     if item['shorts_kor']:
            #         shorts_texts = shorts_texts + item['shorts_kor']
            #         # print(item)
            #     elif item['shorts']:
            #         shorts_texts = shorts_texts + item['shorts']
                        
                 
                # print(shorts_texts)
                # 각 텍스트 앞에 번호를 붙여서 출력
                # prom_text = ''
                # for index, text in enumerate(obj.gemini, start=1):
                #     prom_text = prom_text + f"{index}. {text['shorts']}" +'\n'
            result_list=[]
            result = {}
            gemini_handler = GeminiHandler(obj)
            shorts_texts = gemini_handler.retrieve_texts()
            tag = get_title_tags(text_list=[shorts_texts])
            title = gemini_handler.get_title_run()
            seo = gemini_handler.get_seo_run(shorts_texts)
            result['tag'] = tag
            result['title'] = title
            result['seo'] = seo
            
            print(result)
            result_list.append(result)
            obj.ai_title_tag_article = result_list
            db.commit()
            print('완료')
            logger.info(f"username : {obj.user.username} / title : {obj.title} / auto_get_title_tag_article_scikit_llm complete")
            
        except Exception as e:
            # 오류 발생 시 세션 롤백
            # db.delete(obj)
            if obj.gemini_text_failed_count is None:
                obj.gemini_text_failed_count = 1
            else:
                obj.gemini_text_failed_count += 1
            db.commit()
            logger.error(f"username : {obj.user.username} / title : {obj.title} / auto_get_title_tag_article_scikit_llm failed")
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
    
