import pickle
from pathlib import Path
import pandas as pd

import streamlit as st  
import streamlit_authenticator as stauth 
import index

names = ["yoonhyung jang", "doowon kim", "jinhak choi"]
usernames = ["yhj", "dwk", "jhc"]
# 비밀번호 =  [123,   456,   789]

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
    print("you logged in!")