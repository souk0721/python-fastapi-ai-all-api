import pathlib
import textwrap
import google.generativeai as genai
from packages.database.db import *
from packages.database.models import *
from dotenv import dotenv_values
from pathlib import Path
import requests
from datetime import datetime
import deepl
# from packages.utils.nltk_token_count import tokenize_and_check

# from package.process.utils import create_final_destination_path
# from package.elevenlabs_api.elevenlabs_create_voice import generate_and_play_audio
import os,time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap




class GeminiHandler:
    def __init__(self,obj):
        config = dotenv_values(".env")
        GOOGLE_API_KEY = config.get('GEMINI_API_KEY')
        DEEPL_API_KEY = config.get('DEEPL_API_KEY')
        self.translator = deepl.Translator(DEEPL_API_KEY)
        self.obj = obj
        self.google_api_key = GOOGLE_API_KEY
        self.db_session = SessionLocal()
        self.lim = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=self.google_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.model_name = "jhgan/ko-sbert-nli"
        self.model_kwargs = {'device': 'cuda:0'}
        self.encode_kwargs = {'normalize_embeddings': True}
        self.hf = HuggingFaceEmbeddings(model_name=self.model_name, model_kwargs=self.model_kwargs, encode_kwargs=self.encode_kwargs)
        self.prompt_template = """
            Answer the question as based only on the following context:
            {context}

            Question: {question}
        """

    def retrieve_texts_shorts(self):
        obj = self.obj
        shorts_texts = ''
        if obj:
            for item in obj.gemini:
                shorts_texts += item['shorts_kor'] if item['shorts_kor'] else item['shorts']
        return shorts_texts
    
    # def get_short_text(self,json_data,text_count):
    #     chunk_index = []
    #     current_paragraph = ''
    #     for index,item in enumerate(json_data):
    #         current_paragraph += str(f" {{'text' : '{item['text']}'}}")     
    #         current_paragraph += str(f" {{'start' : '{item['start']}'}}")     
    #         current_paragraph += str(f" {{'end' : '{item['end']}'}}")       
    #         if len(current_paragraph) > text_count:
    #             chunk_index.append(index)
    #             # print('index : ' + str(index))
    #             # print(current_paragraph)
    #             current_paragraph=''
        
        
        
    #     # 마지막 남은 데이터 처리
    #     if current_paragraph:
    #         chunk_index.append(len(json_data) - 1)
    #         print('index : ' + str(len(json_data) - 1))
    #         # print(current_paragraph)
    #     print(chunk_index)
        
    #     ranges = []

    #     # 첫 번째 구간의 시작점은 0
    #     start = 0

    #     for end in chunk_index:
    #         # 각 구간은 start부터 end까지 (end는 포함하지 않음)
    #         ranges.append((start, end))

    #         # 다음 구간의 시작점은 현재 구간의 끝점 + 1
    #         start = end + 1

    #     # 결과 출력
    #     # complete_result = []
    #     result_list =[]
    #     for start, end in ranges:
    #         result_json = {}
    #         print(json_data[start]['start'])
    #         print(json_data[end]['end'])
    #         result_json['start'] = json_data[start]['start']
    #         result_json['end'] = json_data[end]['end']
    #         data = ""
    #         print(f"{json_data[start]}번부터 {json_data[end]}번까지")
    #         for i in range(start, end + 1):
    #             if i < len(json_data):
    #                 # print(json_data[i])  # 혹은 원하는 형태로 json_data[i] 처리
    #                 data += str(json_data[i]['text'])
    #             else:
    #                 break  # json_data의 길이를 초과하는 경우 반복문 종료
    #         ## GPT 사용
    #         # result_json['shorts_eng'] = summerize([data])
    #         ## Gemini 사용
    #         retriever = self.process_texts(data)
    #         question = '15자이내로 요약해줘'
    #         response = self.generate_response(question, retriever)
            
    #         result_json['shorts_kor'] = response
    #         time.sleep(1)
    #         ## deepl로 변역
    #         kr_translate = self.translator.translate_text(result_json['shorts_kor'], target_lang="EN-US")
    #         result_json['shorts_eng'] = kr_translate.text
    #         # print(result.text)  # "Bonjour, le monde !"
    #         result_list.append(result_json)
        
    #     return result_list
    
    def retrieve_texts(self):
        obj = self.obj
        shorts_texts = ''
        if obj:
            for item in obj.gemini:
                shorts_texts += item['shorts_kor'] if item['shorts_kor'] else item['shorts']
        return shorts_texts

    def process_texts(self, shorts_texts):
        texts = self.text_splitter.split_text(shorts_texts)
        docsearch = Chroma.from_texts(texts, self.hf)
        retriever = docsearch.as_retriever(search_type="mmr", search_kwargs={'k':3, 'fetch_k': 10})
        return retriever

    def generate_response(self, question, retriever):
        chain = RunnableMap({
            "context": lambda x: retriever.get_relevant_documents(x['question']),
            "question": lambda x: question
        }) | ChatPromptTemplate.from_template(self.prompt_template) | self.lim
        return chain.invoke({'question': question}).content

    def get_short_doc(self):
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.chains.combine_documents.stuff import StuffDocumentsChain
        from langchain.chains import ReduceDocumentsChain
        from langchain.chains import MapReduceDocumentsChain
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader("노현석_BPO_23년 연찬사용 계회서.pdf")
        document = loader.load()
        document[0].page_content[:200]
        
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n\n",  # 분할기준
        chunk_size=3000,   # 사이즈
        chunk_overlap=500, # 중첩 사이즈
        )
        # 분할 실행
        split_docs = text_splitter.split_documents(document)
        map_template = """다음은 문서 중 일부 내용입니다
        {pages}
        이 문서 목록을 기반으로 주요 내용을 요약해 주세요.
        답변:"""
        # Map 프롬프트 완성
        map_prompt = PromptTemplate.from_template(map_template)
        # Map에서 수행할 LLMChain 정의
       
        map_chain = LLMChain(llm=self.lim, prompt=map_prompt)
        
        # Reduce 단계에서 처리할 프롬프트 정의
        reduce_template = """다음은 요약의 집합입니다:
        {doc_summaries}
        이것들을 바탕으로 통합된 요약을 만들어 주세요.
        답변:"""
        # Reduce 프롬프트 완성
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        # Reduce에서 수행할 LLMChain 정의
        reduce_chain = LLMChain(llm=self.lim, prompt=reduce_prompt)
        
        # 문서의 목록을 받아들여, 이를 단일 문자열로 결합하고, 이를 LLMChain에 전달합니다.
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain,                
            document_variable_name="doc_summaries" # Reduce 프롬프트에 대입되는 변수
        )
                # Map 문서를 통합하고 순차적으로 Reduce합니다.
        reduce_documents_chain = ReduceDocumentsChain(
            # 호출되는 최종 체인입니다.
            combine_documents_chain=combine_documents_chain,
            # 문서가 `StuffDocumentsChain`의 컨텍스트를 초과하는 경우
            collapse_documents_chain=combine_documents_chain,
            # 문서를 그룹화할 때의 토큰 최대 개수입니다.
            token_max=4000,
        )
        # 문서들에 체인을 매핑하여 결합하고, 그 다음 결과들을 결합합니다.
        map_reduce_chain = MapReduceDocumentsChain(
            # Map 체인
            llm_chain=map_chain,
            # Reduce 체인
            reduce_documents_chain=reduce_documents_chain,
            # 문서를 넣을 llm_chain의 변수 이름(map_template 에 정의된 변수명)
            document_variable_name="pages",
            # 출력에서 매핑 단계의 결과를 반환합니다.
            return_intermediate_steps=False,
        )
                # Map-Reduce 체인 실행
        # 입력: 분할된 도큐먼트(②의 결과물)
        result = map_reduce_chain.run(split_docs)
        # 요약결과 출력
        print(result)
        
    def get_seo_run(self,shorts_texts):
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
        from langchain.chains.combine_documents.stuff import StuffDocumentsChain
        from langchain.chains import ReduceDocumentsChain
        from langchain.chains import MapReduceDocumentsChain
        from langchain.docstore.document import Document
        from langchain_community.document_loaders import PyPDFLoader,TextLoader
        # 질문 템플릿 형식 정의
        template = """다음은 기사에 대한 요약본입니다. 
        다음의 내용을 SEO 형식으로 작성해 주세요. 

        SEO 형식은 다음과 같습니다:

        주제: 글을 주된 내용의 제목을 작성한다.
        소제목: 글의 내용을 평가해 보기도 하며, 글의 내용을 적절하게 작성한다.
        내용:
        소제목: 글의 내용을 평가해 보기도 하며, 글의 내용을 적절하게 작성한다.
        내용:
        결론: 글의 내용을 정리하며, 교훈을 적어두기도 한다. 그리고 끝글은 지루하지 않도록 산뜻하게

        {text}

        답변:
        """

        # 템플릿 완성
        prompt = PromptTemplate(template=template, input_variables=['text'])

        # 연결된 체인(Chain)객체 생성
        llm_chain = LLMChain(prompt=prompt, llm=self.lim)

        output = llm_chain.run(text=shorts_texts)
        return output
        # print(output)
    
    def get_title_run(self):
        question = '15글자이내로 제목을 작성해줘'
        shorts_texts = self.retrieve_texts_shorts()
        retriever = self.process_texts(shorts_texts)
        response = self.generate_response(question, retriever)
        return response

# Initialize the GeminiHandler class
# Create the database session




