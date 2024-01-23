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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("노현석_BPO_23년 연찬사용 계회서.pdf")

pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(pages)

from langchain_community.embeddings import HuggingFaceEmbeddings

model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cuda:0'}
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

docsearch = Chroma.from_documents(texts, hf)

retriever = docsearch.as_retriever(
                                    search_type="mmr",
                                    search_kwargs={'k':3, 'fetch_k': 10})
# print(retriever.get_relevant_documents("제주도"))

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap

template = """Answer the question as based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

gemini = ChatGoogleGenerativeAI(model="gemini-pro", temperature = 0,google_api_key=GOOGLE_API_KEY)

chain = RunnableMap({
    "context": lambda x: retriever.get_relevant_documents(x['question']),
    "question": lambda x: x['question']
}) | prompt | gemini

print(chain.invoke({'question': "제목을 15자 이내로 작성해줘"}).content)

