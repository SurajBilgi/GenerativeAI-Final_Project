import streamlit as st
import requests
import time

st.title("ChatBot")

text = st.text_area("Enter text:", "Hello")
cols1, cols2 = st.columns(2)
api_data = None

if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False

if st.button("Search", disabled=st.session_state.button_disabled):
    with st.spinner("Wait for it..."):
        api_data = requests.post("http://127.0.0.1:8000/search", json={"text": text})


if api_data:
    answer = api_data.json()["answer"]
    st.markdown(answer)
