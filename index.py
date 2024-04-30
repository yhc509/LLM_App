import streamlit as st
import pandas as pd

import langwrapper as llm

def add_message(prompt, uploadedFile):
    st.session_state.messages.append({"role" : "USER", "content" : prompt})
    res = llm.Prompt(st.session_state.model, prompt, uploadedFile)
    st.session_state.messages.append({"role" : "BOT", "content" : res})

def main():
    st.set_page_config(page_title="Test Chat-Bot Page")

    st.title("CHAT BOT")

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

if __name__ == '__main__':
    main()