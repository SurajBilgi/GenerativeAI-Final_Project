import streamlit as st

st.set_page_config(
    page_title="DineMate",
    page_icon="👨‍🍳",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Welcome to DineMate👨‍🍳")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/restaurants.py", label="Restaurants", icon="🏠")

with col2:
    st.page_link("pages/chat.py", label="Chat", icon="💬")

with col3:
    st.page_link("pages/complaint.py", label="Complaint", icon="🗣️")
