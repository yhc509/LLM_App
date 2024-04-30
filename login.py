import streamlit as st
import streamlit_authenticator as stauth 
from pathlib import Path
import pickle


class LoginPage:

    # 임시 아이디, 비밀 번호
    names = ["yoonhyung jang", "doowon kim", "jinhak choi"]
    usernames = ["yhj", "dwk", "jhc"]
    # 비밀번호 =  [123,   456,   789]
    currAuth = ""

    def ShowLoginPageAndCheckAthentication(self):
        # hashed passwords 불러오기
        file_path = Path(__file__).parent / "hashed_pw.pkl"
        with file_path.open("rb") as file:          # rb : read binary mode
            hashed_passwords = pickle.load(file)
        self.currAuth = stauth.Authenticate(LoginPage.names, LoginPage.usernames, hashed_passwords, 
            "sales_dashboard", "abcdef", cookie_expiry_days=30) # 쿠키에 저장되어 리프레시 후에 로긴이 지속됨
        
        name, authentication_status, username = self.currAuth.login("Login", "main") # 로그인

        return authentication_status

