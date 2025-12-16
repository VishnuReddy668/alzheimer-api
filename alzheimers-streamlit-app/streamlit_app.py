import streamlit as st
import requests

st.set_page_config(page_title="Alzheimer Detection", layout="centered")

st.title("🧠 Alzheimer Detection")
st.write("Upload a handwritten image to predict")

uploaded_file = st.file_uploader(
    "Upload handwriting image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict"):
        with st.spinner("Analyzing..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(
                "https://alzheimer-image-api.onrender.com/predict",
                files=files
            )

            if response.status_code == 200:
                result = response.json()["prediction"]

                if result == "P":
                    st.error("⚠️ Alzheimer / Cognitive Risk Detected")
                else:
                    st.success("✅ No Cognitive Impairment Detected")
            else:
                st.error("Server error. Try again.")
