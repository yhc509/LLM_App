import dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import chroma
from langchain.vectorstores import Chroma
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain.schema.runnable import RunnablePassthrough
from langchain import hub
from langchain.chains import RetrievalQA

# load .env
dotenv.load_dotenv()

params = {
    "temperature": 1,           # 생성된 텍스트의 다양성 조정
    "max_tokens": 100,          # 생성할 최대 토큰 수
}

kwargs = {
    "frequency_penalty": 0.5,   # 이미 등장한 단어의 재등장 확률
    "presence_penalty": 0.5,    # 새로운 단어의 도입을 장려
    "stop": ["\n"]              # 정지 시퀀스 설정

}

def InitModel():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125", 
        **params, 
        model_kwargs = kwargs,
        )
    conv = ConversationSummaryBufferMemory(
        llm=llm, 
        max_token_limit=100,
        )
    conversation = ConversationChain(
        llm=llm, 
        memory = conv,
        verbose=True,
    )
    return conversation
    

def ReadFile(uploaded_file):
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_file.getvalue())
        file_name = uploaded_file.name
    
    loader = PyPDFLoader(temp_file)
    documents = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    db = Chroma.from_documents(documents=texts, embedding=embeddings)
    retriever = db.as_retriever()
    return retriever

def Prompt(model, prompt, uploadedFile):
    if uploadedFile is not None:
        retriever = ReadFile(uploadedFile)
        promptTemplate = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a helpful assistant. 
                    Answer questions using only the following context. 
                    If you don't know the answer just say you don't know, don't make it up:
                    \n\n
                    {context}",
                    """
                ),
                ("human", "{question}"),
            ]
        )

        llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125", 
            **params, 
            model_kwargs = kwargs,
        )
        chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
            | promptTemplate
            | llm
            | StrOutputParser()
        )
        output = chain.invoke(prompt)
        # output = model.invoke({"context": retriever, "input":prompt})
        # p = hub.pull("rlm/rag-prompt")
        # qa_chain = RetrievalQA.from_chain_type(
        #     model,
        #     retriever=retriever,
        #     chain_type_kwargs={"prompt": p}
        # )
        # output = qa_chain(query=prompt)
    else:
        output = model.predict(input=prompt)
    return output
