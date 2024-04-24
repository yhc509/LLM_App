import dotenv
import os
import asyncio

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

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
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", **params, model_kwargs = kwargs)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

def Prompt(req):
    conversation = ConversationChain(
        llm=llm, 
        memory = memory,
        verbose=True
    )
    output = conversation.predict(input=req)
    return output
