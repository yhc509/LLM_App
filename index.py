import streamlit as st
import pandas as pd

st.title('My first app')
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))




# Test code
# import langwrapper as lw

# print(lw.Prompt("강아지와 고양이가"))