import dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

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

def Prompt(conv, req):
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 30대 초반의 남성입니다. 친구처럼 대답해주세요."),    # 챗봇에게 역할을 지정한다.
        ("user", "{input}"),    # 유저의 질의 메세지
    ])
    chain = chat_prompt | llm | StrOutputParser()
    output = chain.invoke({"input": {req}})
    return output
