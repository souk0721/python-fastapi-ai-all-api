from openai import OpenAI
from pathlib import Path
import json,re
# from package.bard_api.text_json import JsonExtractor
from dotenv import dotenv_values
from pathlib import Path
import requests
from datetime import datetime
# from package.process.utils import create_final_destination_path
# from package.elevenlabs_api.elevenlabs_create_voice import generate_and_play_audio
import os
config = dotenv_values(".env")
OPENAI_API_KEY = config.get('OPENAI_API_KEY')

class ChatGPTApi:
    def __init__(self):
        dotenv_values(".env")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.base_path = Path(__file__).parent
        self.imgs_path = 'static/imgs/'
        self.voices_path = 'static/audio/'
        self.current_time = datetime.now().strftime("%Y%m%d_%H%M")
    
    def create_img(self,text,title):
        
        directory_path = self.base_path / '..' / 'flask' / 'static' / 'imgs' / title
        directory_path.mkdir(parents=True, exist_ok=True)
        safe_text = re.sub(r'[\\/*?:"<>|\n]', '-', text)
        img_file_path = directory_path / f"{safe_text}_{self.current_time}.png"
        
        response = self.client.images.generate(
        model="dall-e-3",
        prompt=text+'이 텍스트를 기반으로 읿본 애니메이션 스타일로 이미지 생성해줘',
        size="1792x1024",
        quality="standard",
        n=1,
        )

        image_url = response.data[0].url
        # 이미지 다운로드
        response = requests.get(image_url)
        # 요청이 성공적으로 완료되었는지 확인
        if response.status_code == 200:
            # 이미지 데이터를 파일로 저장
            with open(img_file_path, 'wb') as file:
                file.write(response.content)
        else:
            print("이미지 다운로드 실패:", response.status_code)
        return f"{self.imgs_path}{title}/{safe_text}_{self.current_time}.png"
        
    def get_voice(self,text,title):
        
         # 파일 이름으로 사용할 수 없는 문자를 대체
        directory_path = self.base_path / '..' / 'flask' / 'static' / 'audio' / title
        # directory_path = Path(__file__).parent / title
        directory_path.mkdir(parents=True, exist_ok=True)  # 디렉토리가 없으면 생성
        safe_text = re.sub(r'[\\/*?:"<>|\n]', '-', text)
        print(safe_text)
        self.speech_file_path = directory_path / f"{safe_text}.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
        )
        response.stream_to_file(self.speech_file_path)
        return f"{self.voices_path}{title}/{safe_text}.mp3"
    
    # def get_voice_eleven(self,text,title,directory_path,who):
        
    #      # 파일 이름으로 사용할 수 없는 문자를 대체
    #     directory_path= directory_path
    #     safe_text = re.sub(r'[\\/*?:"<>|\n]', '-', title)
    #     print(safe_text)
    #     self.speech_file_path = os.path.join(directory_path , f"{safe_text}.mp3")
    #     # 함수 사용 예시
    #     get_voice = generate_and_play_audio(
    #         text=text,
    #         voice_id=who,
    #         stability=0.71,
    #         similarity_boost=0.5,
    #         style=0.0,
    #         use_speaker_boost=True
    #     )
           
    #     # # Saving the audio for later
        
    #     with open(self.speech_file_path, 'wb') as f:
    #         f.write(get_voice)
        
    #     # response = self.client.audio.speech.create(
    #     #     model="tts-1",
    #     #     voice="nova",
    #     #     input=text,
    #     # )
    #     # response.stream_to_file(self.speech_file_path)
    #     return self.speech_file_path
    
    def youtube_get_voice(self,text,title,directory_path,who):
        
         # 파일 이름으로 사용할 수 없는 문자를 대체
        directory_path= directory_path
        safe_text = re.sub(r'[\\/*?:"<>|\n]', '-', title)
        print(safe_text)
        self.speech_file_path = os.path.join(directory_path , f"{safe_text}.mp3")
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=who,
            input=text,
        )
        response.stream_to_file(self.speech_file_path)
        return self.speech_file_path
    
    def get_blog_jon(self,text):
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "너는 SEO 형식에 맞춰 블로그를 작성하는 전문가이다.JSON 형식으로 출력해줘"},
            {"role": "user", "content": f"{text}->이 텍스트를 참고하여 SEO 형식에 맞게 title, content 블로그 작성해줘"}
        ]
        )
        return response.choices[0].message.content


    
    def ai_fix_openai(self,text):
        prompt='''
                아래의 글을 참고하여 주제는 10자 이내로 작성하고, 
                컨텐츠는 아래의 글을 참고하여 너의 지식을 사용하여 무서운 글을 작성해줘, 
                그리고 한 문장은 15 ~ 20자 이내로 하고 줄바꿈해줘. 
                그리고 아래의 형식에 맞게 joson형식으로 작성해줘. 
                글을 잘 작성하면 너에게 팁을 200$ 줄께 신경써서 작성해줘
                {
                    "title": 주제,
                    "content": 컨텐츠
                }
                아래의 글 /n
                ''' 
        
        
        sentences = text
        paragraph = []
        current_paragraph = ''
        for sentence in sentences:
            result_json = {}
            current_paragraph += sentence 
            # print("current_paragraph : " + current_paragraph)
            # 문단의 길이가 1000자를 초과하면 새로운 문단으로 생성
            if len(current_paragraph) > 1000:
                
                print("current_paragraph : " + current_paragraph)
                prompt = prompt + current_paragraph
                completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
                                                # 보낼 메세지 목록
                                                messages=[{"role": "system", "content":"넌 무서운 이야기를 만드는 작가야"},
                                                        {"role": "user", "content": prompt}]) # 사용자
                
                result = completion.choices[0].message.content
                # result = json.dumps(result)
                result = json.loads(result)
                # print(result)
            
                # print(result['title'])
                # print(result['content'])
                # # time.sleep(30)
                    
                # content = notion_ai.summarize(context=current_paragraph)
                # print("content : " + content)
                # time.sleep(30)
                
                # # 현재 문단을 문단 리스트에 추가
                result_json['title']= result['title']
                result_json['content'] = result['content']
                paragraph.append(result_json)
                
                # 새로운 문단을 시작
                current_paragraph = ''
                # time.sleep(5)
        # print(current_paragraph)
        if current_paragraph:
            prompt = prompt + current_paragraph
            completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
                                                    # 보낼 메세지 목록
                                                messages=[{"role": "system", "content":"넌 이야기 컨텐츠 유튜버야"},
                                                        {"role": "user", "content": prompt}]) # 사용자
                
            result = completion.choices[0].message.content
            # result = json.dumps(result)
            result = json.loads(result)
            # print(result)
            
            # print(result['title'])
            # print(result['content'])
            # # time.sleep(30)
                    
            # content = notion_ai.summarize(context=current_paragraph)
            # print("content : " + content)
            # time.sleep(30)
            
            # # 현재 문단을 문단 리스트에 추가
            result_json['title']= result['title']
            result_json['content'] = result['content']
            paragraph.append(result_json)
        return result_json
    def ai_fix_text(self,text):
        prompt='''
                아래의 글을 참고하여 주제는 10자 이내로 작성하고, 
                컨텐츠는 아래의 글을 참고하여 너의 지식을 사용하여 무서운 글을 작성해줘, 
                그리고 한 문장은 15자 이내로 하고 줄바꿈해줘. 
                그리고 아래의 형식에 맞게 joson형식으로 작성해줘. 
                글을 잘 작성하면 너에게 팁을 200$ 줄께 신경써서 작성해줘
                {
                    "title": 주제,
                    "content": 컨텐츠
                }
                아래의 글 /n
                ''' 
        
        
        sentences = text
        paragraph = []
        current_paragraph = ''
        for sentence in sentences:
            result_json = {}
            current_paragraph += sentence 
            # print("current_paragraph : " + current_paragraph)
            # 문단의 길이가 1000자를 초과하면 새로운 문단으로 생성
            if len(current_paragraph) > 1000:
                
                print("current_paragraph : " + current_paragraph)
                prompt = prompt + current_paragraph
                completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
                                                # 보낼 메세지 목록
                                                messages=[{"role": "system", "content":"넌 전문적인 소설가이다."},
                                                        {"role": "user", "content": prompt}]) # 사용자
                
                result = completion.choices[0].message.content
                # result = json.dumps(result)
                result = json.loads(result)
                # print(result)
            
                # print(result['title'])
                # print(result['content'])
                # # time.sleep(30)
                    
                # content = notion_ai.summarize(context=current_paragraph)
                # print("content : " + content)
                # time.sleep(30)
                
                # # 현재 문단을 문단 리스트에 추가
                result_json['title']= result['title']
                result_json['content'] = result['content']
                paragraph.append(result_json)
                
                # 새로운 문단을 시작
                current_paragraph = ''
                # time.sleep(5)
        # print(current_paragraph)
        if current_paragraph:
            prompt = prompt + current_paragraph
            completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
                                                    # 보낼 메세지 목록
                                                messages=[{"role": "system", "content":"넌 전문적인 소설가이다."},
                                                        {"role": "user", "content": prompt}]) # 사용자
                
            result = completion.choices[0].message.content
            # result = json.dumps(result)
            result = json.loads(result)
            # print(result)
            
            # print(result['title'])
            # print(result['content'])
            # # time.sleep(30)
                    
            # content = notion_ai.summarize(context=current_paragraph)
            # print("content : " + content)
            # time.sleep(30)
            
            # # 현재 문단을 문단 리스트에 추가
            result_json['title']= result['title']
            result_json['content'] = result['content']
            paragraph.append(result_json)
        return result_json
    
    def ai_shorts(self,text):
        reuslt_list =[]
        result_json = {}
        prompt='''
        아래의 리스트는 동영상의 start 시간과 end 시간 그리고 text가 있다. 
        1. 주어진 리스트의 'text'를 참고하여 title을 작성한다. title은 50자 미만으로 작성한다.
        2. 주어진 리스트의 'text'를 참고하여 tag를 작성한다. tag는 5개 이하로 한다.
            ex) tag =['ai','정치','사회','경제','상품리뷰','재미있는 이야기','애니리뷰','영화리뷰'] 
        3. 주어진 리스트의 'text'를 이어붙여 500자이하로 만들고 그내용을 shorts에 저장한다.
        4. shorts에저장된 내용의 'start', 'end'를 파악한다.
        5. 무조건 JSON 형식으로 작성한다. 예를 들어
        [
            {
                'title' : '전체 내용의 title'
                'tag' : ['ai','교육','정치','사회']
                'data'  : [
                    {
                        "start" : "7.5"
                        "shorts" : "내용요약"
                        "end" : "100.7"
                    },
                    {
                        "start" : "120.5"
                        "shorts" : "내용요약"
                        "end" : "200.8"
                    },
                ]
            }
        
        ]
        
        아래의 글 /n
        ''' + text
        completion = self.client.chat.completions.create(model="gpt-3.5", # 사용할 모델
                                        # 보낼 메세지 목록
                                        messages=[{"role": "system", "content":"너는 데이터를 json 형태로 작성한는 전문가이다. 나를 도와줘"},
                                                {"role": "user", "content": prompt}]) # 사용자
        
        result = completion.choices[0].message.content
        print(result)
        result = json.loads(result)
        # result_json['start']= result['start']
        # result_json['shorts'] = result['shorts']
        # result_json['end'] = result['end']
        # reuslt_list.append()
        return result
    
    def ai_openai_poem(self,text):
        result_json = {}
        prompt='''
        아래의 글은 노래가사이다. 참고하여 주제는 10자 이내로 작성하고, 컨텐츠는 500자이내로 노래가사를 해석해서 작성하고, 
        아래의 형식에 맞게 json형식으로 작성해줘, 한국어로 작성해줘 
        재미있게 작성해줘, 공감가게 작성해줘, 반복 문장은 2개이상 작성하지마.
        {
            "title": 주제,
            "content": 컨텐츠
        }
        아래의 글 /n
        ''' + text
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
                                        # 보낼 메세지 목록
                                        messages=[{"role": "system", "content":"너는 대중문화를 전문으로하는 작가이다. 나를 도와줘"},
                                                {"role": "user", "content": prompt}]) # 사용자
        
        result = completion.choices[0].message.content
        result = json.loads(result)
        result_json['title']= result['title']
        result_json['content'] = result['content']
        return result_json
    
    def ai_scenes_create(self,text):
        result_json = {}
        prompt='''
            나는 유튜브 숏츠를 만들려고 한다. 상황에 맞는 장면을 추가하려고 한다.
            내가 제공하는 문장으로 아래의 예시처럼 작성해줘.  
            아래의 예시와 같이 JSON 형식으로 작성해주세요.
            description은 상황에 맞는 장면을 상상하여 영어로 작성해줘
            예시 : 
            주어진 문장 :
            0 : 최근 이사 온 윗집 주민들의
            1 : 무분별한 소음 때문에 매일 밤 잠을 이루지 못한다.
            2 : 윗집은 한 가족이 살고 있는데,
            3 : 두 아이가 있는 가정이다.
            4 : 아이들은 뛰고, 떠들고,
            5 : 장난감을 바닥에 던지며 놀기를 즐긴다.
            6 :  현수는 그 소리에 시달리며 점점 지쳐간다.
            7 : 어느 날, 현수는 참다못해 윗집에 항의하러 간다. 문을 두드리자,
            8 : 윗집 아이들의 엄마가 문을 연다.
            9 : 현수는 격앙된 목소리로 층간 소음에 대해 이야기한다.
            10 : 윗집 엄마는 처음엔 미안하다며 사과하지만,
            11 : 아이들을 통제하는 것이 쉽지 않다며
            12 : 난처한 표정을 짓는다.
            13 : 대화는 서로의 입장만을 고집하는 싸움으로 번진다.
            14 : 현수는 욕설을 내뱉으며 분노를 표출하고,
            15 : 윗집 엄마도 목소리를 높이며 반박한다.
            16 : 결국, 두 사람은 합의점을 찾지 못하고 갈등은 더욱 깊어진다.
            17 :  현수는 자신의 권리를 침해받았다고 느끼며 분노하고,
            18 : 윗집 엄마는 아이들을 키우며 겪는 어려움을 이해받지 못한다고 생각 한다.
            19 : 이 이야기는 층간 소음이라는
            20 : 사소해 보이는 문제가 어떻게
            21 : 강렬한 감정의 충돌로 이어질 수 있는지를 보여준다.
            22 : 양측 모두의 입장이 이해될 수 있는 상황에서,
            23 : 여러분은 이 갈등 상황에 어떻게 대처하시겠습니까?

            예시 : 
            {
                "scenes": [
                    {
                        "index": "0",
                        "description": "The protagonist struggling to sleep at night due to the noise from the new upstairs neighbors"
                    },
                    {
                        "index": "5",
                        "description": ""Upstairs children playing joyfully, throwing toys on the floor, creating noise"
                    },
                    {
                        "index": "8",
                        "description": "A resident knocking on the door and the mother of the upstairs children opening it"
                    },
                    {
                        "index": "15",
                        "description": "A heated confrontation between the downstairs resident and the upstairs mother, both raising their voices."
                    },
                    {
                        "index": "23",
                        "description": "The scene showing the escalation of the conflict, with narration asking the audience for their approach to such a situation."
                    }
                   
                ]
            }
            주어진 문장:
        ''' + text
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo", # 사용할 모델
                                        # 보낼 메세지 목록
                                        messages=[{"role": "system", "content":"너는 나를 도워주는 ai이다."},
                                                {"role": "user", "content": prompt}]) # 사용자
        
        result = completion.choices[0].message.content
        result = json.loads(result)
        # result_json['scenes']= result['scenes']
        # result_json['content'] = result['content']
        return result
# test = ChatGPTApi()
# test.get_voice()   