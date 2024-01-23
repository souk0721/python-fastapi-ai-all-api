from packages.database.db import *
from packages.database.models import *
db = SessionLocal()

obj = get_all_entries(db=db,model_class=YoutubeFile)
for i in obj:
    i.gemini_text_failed_count = 0
    i.gemini_title_tag_failed_count = 0
    # i.gpt = None
    # i.notion = None
    # i.ai_title_tag_article = None
db.commit()
db.close ()

    
    
    # print(i.gemini_text_failed_count)
