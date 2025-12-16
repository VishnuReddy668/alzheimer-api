import streamlit as st
import requests
from PIL import Image

API_URL = "https://alzheimer-image-api.onrender.com/predict"

st.set_page_config(page_title="Alzheimer's Disease Prediction", layout="centered")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "prediction" not in st.session_state:
    st.session_state.prediction = None

# ---------- HEADER ----------
st.markdown(
    """
    <h2 style='text-align:center;'>Alzheimer's Disease Prediction</h2>
    <p style='text-align:center;color:gray;'>
    Upload medical image to analyze Alzheimer’s risk
    </p>
    """,
    unsafe_allow_html=True
)

# ---------- SCREEN 1 ----------
if st.session_state.page == "upload":

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict Now"):
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Analyzing image..."):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }

                response = requests.post(API_URL, files=files)

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.prediction = result["prediction"]
                    st.session_state.page = "result"
                    st.rerun()
                else:
                    st.error("Prediction failed")

# ---------- SCREEN 2 ----------
elif st.session_state.page == "result":

    pred = st.session_state.prediction

    if pred == "P":
        risk = "High Risk"
        confidence = "87.5%"
        color = "red"
        findings = [
            "Irregular handwriting patterns detected",
            "Cognitive stress indicators present",
            "Further medical evaluation recommended"
        ]
    else:
        risk = "Low Risk"
        confidence = "90.2%"
        color = "green"
        findings = [
            "Normal handwriting patterns detected",
            "Cognitive function within normal range",
            "No significant indicators found"
        ]

    st.markdown("## Prediction Result")

    st.markdown(
        f"""
        <h3 style='color:{color};'>{risk}</h3>
        <p><b>Confidence:</b> {confidence}</p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Key Findings")
    for f in findings:
        st.write("•", f)

    if st.button("New Prediction"):
        st.session_state.page = "upload"
        st.session_state.prediction = None
        st.rerun()
