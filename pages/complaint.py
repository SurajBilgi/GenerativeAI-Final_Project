import streamlit as st
from PIL import Image
import io
import requests

st.title("Complaint Bot")

complaint = st.text_input("Kindly type your complaint")
img = st.file_uploader(
    "Upload Customer Image", type=["jpg", "jpeg", "png"], help="Limit 20MB per file"
)
ref_img = st.file_uploader(
    "Upload Reference Image", type=["jpg", "jpeg", "png"], help="Limit 20MB per file"
)
if st.button("Submit"):
    if img is not None and ref_img is not None:
        with st.spinner("Wait for it..."):
            customer_image = Image.open(img)
            customer_img_bytes = io.BytesIO()
            customer_image.save(customer_img_bytes, format=customer_image.format)
            customer_img_bytes = customer_img_bytes.getvalue()

            ref_image = Image.open(ref_img)
            ref_img_bytes = io.BytesIO()
            ref_image.save(ref_img_bytes, format=ref_image.format)
            ref_img_bytes = ref_img_bytes.getvalue()

            files = {
                "cust_file": ("cust_image.jpg", customer_img_bytes, "image/jpeg"),
                "ref_file": ("ref_image.jpg", ref_img_bytes, "image/jpeg"),
            }

            data = {"text": complaint}

            response = requests.post(
                "http://127.0.0.1:8000/complaint", files=files, data=data
            )
            response = response.json()

            if response["is_complaint_genuine"]:
                st.success(response["image_description"], icon=None)
                st.success("A refund will be immediately initiated", icon=None)
            else:
                st.error(response["image_description"], icon=None)
                st.error("No refund", icon=None)
    else:
        st.error("Kindly add image", icon=None)
