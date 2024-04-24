import streamlit as st
import pandas as pd

import langwrapper as llm
import asyncio

def add_message(prompt):
    st.session_state.messages.append({"role" : "USER", "content" : prompt})
    res = llm.Prompt(prompt)
    st.session_state.messages.append({"role" : "BOT", "content" : res})
    # st.session_state.converstaion.append({"input":prompt, "output":res})

def main():
    st.set_page_config(page_title="Test Chat-Bot Page")

    st.title("_Test 123 type at the bottom :blue[CHAT]_")

    # 아래껀 뭐하는거지;; 초기화를 해야 제대로 사용한다는데 아직 잘 모르겠다
    # if "converstaion" not in st.session_state:
    #     st.session_state.converstaion = []
    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = None

    # 맨처음 가이드 텍스트
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    

    if query := st.chat_input("Type your question."): # 채팅 텍스트필드
        add_message(query)

    # 파일 업로드 예시
    uploadedFile = st.file_uploader('File uploader')

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if __name__ == '__main__':
    main()