import streamlit as st
import streamlit_authenticator as stauth 

import langwrapper as llm

from pathlib import Path
import pandas as pd

import login

# 임시 아이디, 비밀 번호
names = ["yoonhyung jang", "doowon kim", "jinhak choi"]
usernames = ["yhj", "dwk", "jhc"]
# 비밀번호 =  [123,   456,   789]

def add_message(prompt, uploadedFile):
    st.session_state.messages.append({"role" : "USER", "content" : prompt})
    res = llm.Prompt(st.session_state.model, prompt, uploadedFile)
    st.session_state.messages.append({"role" : "BOT", "content" : res})


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

    # 클래스로 바꿔봄
    loginPage = login.LoginPage()
    authenticationState = loginPage.ShowLoginPageAndCheckAthentication()

    if authenticationState == True:
        st.success("You have been logged in")
        loginPage.currAuth.logout("Logout","main")
        ShowChatBotPage()
    elif authenticationState == None:
        st.warning("Please enter your username and password")
    elif authenticationState == False:
        st.error("Username/password is incorrect")
