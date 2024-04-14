import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Test Chat-Bot Page")

    st.title("_Test 123 type at the bottom :blue[CHAT]_")

    # 아래껀 뭐하는거지;; 초기화를 해야 제대로 사용한다는데 아직 잘 모르겠다
    if "converstaion" not in st.session_state:
        st.session_state.converstaion = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # 맨처음 가이드 텍스트
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role" : "assistant",
                                         "content" : "Hello dude, ask me if you have anything to ask."}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("Type your question."): # 채팅 텍스트필드
        st.session_state.messages.append({"role" : "user", "content" : query}) # 질문 입력한것 출력
        st.session_state.messages.append({"role" : "assistant", "content" : "Dummy answer oh yeah"}) # 더미 텍스트


if __name__ == '__main__':
    main()

st.title('My first app')
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))


