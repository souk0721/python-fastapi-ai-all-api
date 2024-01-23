import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# model_id = "kyujinpy/Ko-PlatYi-6B"
model_id = "microsoft/phi-2"
# model_id = "megastudy/M-SOLAR-10.7B-v1.3"
# model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_id,trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto",trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")

# print(model)

# device = "cuda:0"

# messages = [
#     {"role": "user", "content": "세종 대왕에 대하여 알려줘"}
# ]


# encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

# model_inputs = encodeds.to(device)


# generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
# decoded = tokenizer.batch_decode(generated_ids)
# print(decoded[0])


import locale
def getpreferredencoding(do_setlocale = True):
    return "UTF-8"
locale.getpreferredencoding = getpreferredencoding

from langchain_community.llms.huggingface_pipeline  import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from transformers import pipeline
from langchain.chains import LLMChain

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.7,
    return_full_text=True,
    max_new_tokens=300,
)

prompt_template = """
### [INST]
Instruction: Answer the question based on your knowledge.
Here is context to help:

{context}

### QUESTION:
{question}

[/INST]
 """

koplatyi_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

# Create prompt from prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

# Create llm chain
llm_chain = LLMChain(llm=koplatyi_llm, prompt=prompt)

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain.schema.runnable import RunnablePassthrough

loader = PyPDFLoader("2023년제주도여행계획서.pdf")
pages = loader.load_and_split()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(pages)

from langchain_community.embeddings import HuggingFaceEmbeddings

model_name = "jhgan/ko-sbert-nli"
encode_kwargs = {'normalize_embeddings': True}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)

db = Chroma.from_documents(texts, hf)
retriever = db.as_retriever(
                            search_type="similarity",
                            search_kwargs={'k': 3}
                        )

rag_chain = (
 {"context": retriever, "question": RunnablePassthrough()}
    | llm_chain
)

import warnings
warnings.filterwarnings('ignore')

result = rag_chain.invoke("2일차 아침 부터 12시까지 일정알려줘, 소요되는 시간을 파악하여 알려줘")

for i in result['context']:
    print(f"주어진 근거: {i.page_content} / 출처: {i.metadata['source']} - {i.metadata['page']} \n\n")

print(f"\n답변: {result['text']}")
