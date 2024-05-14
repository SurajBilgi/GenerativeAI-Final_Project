import streamlit as st
from PIL import Image
import io
import requests

st.title("Complaint Bot")

complaint = st.text_input("Kindly type your complaint")
img = st.file_uploader(
    "Upload Image", type=["jpg", "jpeg", "png"], help="Limit 20MB per file"
)
if st.button("Submit"):
    if img is not None:
        image = Image.open(img)

        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format)
        img_bytes = img_bytes.getvalue()

        # Send the image to the API
        url = "http://127.0.0.1:8000/complaint"
        files = {"file": ("image.jpg", img_bytes, "image/jpeg")}
        data = {"text": complaint}
        response = requests.post(url, files=files, data=data)
        response = response.json()
        if response["is_complaint_genuine"]:
            st.success(response["image_description"], icon=None)
        else:
            st.error(response["image_description"], icon=None)
