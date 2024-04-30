import streamlit as st
import streamlit_authenticator as stauth 

import langwrapper as llm

import pickle
from pathlib import Path
import pandas as pd

# 임시 아이디, 비밀 번호
names = ["yoonhyung jang", "doowon kim", "jinhak choi"]
usernames = ["yhj", "dwk", "jhc"]
# 비밀번호 =  [123,   456,   789]

def add_message(prompt):
    st.session_state.messages.append({"role" : "USER", "content" : prompt})
    res = llm.Prompt(st.session_state.model, prompt, uploadedFile)
    st.session_state.messages.append({"role" : "BOT", "content" : res})


def ShowLoginPage():   
    # hashed passwords 불러오기
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:                  # rb : read binary mode
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 
        "sales_dashboard", "abcdef", cookie_expiry_days=30) # 이거 쓰면 쿠키에 저장되어 리프레시 후에 로긴이 지속됨
        # 그런데 한번 로그인 성공하고 껐다가 다시 키면 로그인 시도도 못하고 로그인됨;;

    name, authentication_status, username = authenticator.login("Login", "main") # 로그인

    # 로그인 실패 성공 등의 분기
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status == True:
        #print("you logged in!")
        if __name__ is "__main__":
            ShowChatBotPage() 
            st.success("You have been logged in")
            authenticator.logout("Logout","main")


def ShowChatBotPage():
    # 아래껀 뭐하는거지;; 초기화를 해야 제대로 사용한다는데 아직 잘 모르겠다
    if "model" not in st.session_state:
        st.session_state.model = llm.InitModel()
    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = None

    # 맨처음 가이드 텍스트
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # 파일 업로드 예시
    uploadedFile = st.file_uploader('File uploader')
    
    if query := st.chat_input("Type your question."): # 채팅 텍스트필드
        add_message(query, uploadedFile)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



# 뭔 실행을 이렇게 하지;; 
if __name__ == '__main__':
    st.set_page_config(page_title="Test Chat-Bot Page")

    st.title("_Test 123 type at the bottom :blue[CHAT]_")

    ShowLoginPage()
