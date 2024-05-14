import streamlit as st
import pandas as pd
import requests

col1, col2 = st.columns([1, 3])

restaurant_info = None
with col1:
    restaurant_list = requests.get("http://127.0.0.1:8000/restaurant-list")
    for restaurant in restaurant_list.json()["restaurant_list"]:
        if st.button(
            restaurant,
            key=restaurant,
        ):
            restaurant_info = requests.post(
                "http://127.0.0.1:8000/restaurant-info", data={"text": restaurant}
            )
            restaurant_info = restaurant_info.json()

with col2:
    if restaurant_info:
        df = pd.DataFrame(restaurant_info["restaurant_info"])
        df.columns = ["Type", "Dish", "Cost(in $)", "Prep Time(in Minutes)"]
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
