import dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

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

def Prompt(req):
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 30대 초반의 남성입니다. 친구처럼 대답해주세요."),
        ("user", "{input}"),
    ])
    chain = chat_prompt | llm | StrOutputParser()
    output = chain.invoke({"input": {req}})
    return output
