import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["yoonhyung jang", "doowon kim", "jinhak choi"]
usernames = ["yhj", "dwk", "jhc"]
passwords = ["xxx", "xxx", "xxx"]
hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)