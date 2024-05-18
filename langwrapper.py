import dotenv
import os
import hashlib
from operator import itemgetter

# OpenAI
from langchain_openai import ChatOpenAI

# Chain
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationSummaryBufferMemory

# Embedding, RAG
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# load .env
dotenv.load_dotenv()

class WrapModel:
    llm = None
    conv = None

    params = {
        "temperature": 0.5,           # 생성된 텍스트의 다양성 조정
        "max_tokens": 1000,          # 생성할 최대 토큰 수
    }

    kwargs = {
        "frequency_penalty": 0.5,   # 이미 등장한 단어의 재등장 확률
        "presence_penalty": 0.5,    # 새로운 단어의 도입을 장려
        "stop": ["\n"]              # 정지 시퀀스 설정

    }

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125", 
            **self.params, 
            model_kwargs = self.kwargs,
            )
        self.conv = ConversationSummaryBufferMemory(
            memory_key="chat_memory",
            return_messages=True,
            llm = self.llm, 
            max_token_limit = 4000,
            )
    

def InitModel():
    return WrapModel()
    

def ReadFile(uploaded_file):
    data=uploaded_file.getvalue()
    hash=hashlib.sha256(data).hexdigest()

    temp_file = "./" + hash + ".pdf"

    if os.path.isfile(temp_file) is False:
        with open(temp_file, "wb") as file:
            file.write(data)
    
    loader = PyPDFLoader(temp_file)
    documents = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    cache_dir = LocalFileStore("./.cache/practice/")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    db = FAISS.from_documents(texts, cached_embeddings)
    retriever = db.as_retriever()
    return retriever

def Prompt(model, prompt, uploadedFile):
    retriever = None
    if uploadedFile is not None:
        retriever = ReadFile(uploadedFile)
        
    promptTemplate = ChatPromptTemplate.from_messages([
        ("system", 
         """
         You are a helpful assistant, conversation friend.
         Answer questions using only the following context. 
         If you don't know the answer just say you don't know, don't make it up:
         \n\n
         {context}",
         """
         ),
        MessagesPlaceholder(variable_name="chat_memory"),
        ("human", "{question}"),
    ])

    if retriever is None:
        context = RunnablePassthrough.assign(
            context=itemgetter("question")
        )
    else:
        context = RunnablePassthrough.assign(
            context=itemgetter("question") | retriever,
        )

    chain = (
        context |
        RunnablePassthrough.assign(chat_memory=lambda input : model.conv.load_memory_variables({})["chat_memory"])
        | promptTemplate
        | model.llm
    )
    print(model.conv.load_memory_variables({}))
    output = invoke_chain(chain, model.conv, prompt)
    return output.content

def invoke_chain(chain, memory, question):
    result = chain.invoke({"question": question})
    # memory에 대화 내용을 저장한다.
    memory.save_context(
        {"input": question},
        {"output": result.content},
    )
    return result
