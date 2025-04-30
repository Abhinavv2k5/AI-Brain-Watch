import streamlit as st
from streamlit_option_menu import option_menu
import tensorflow as tf
from PIL import Image
import numpy as np
import base64
import os

# Function to set background image
def set_background(image_path):
    try:
        with open(image_path, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string.decode()}");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Failed to set background: {e}")

# Load the model
try:
    model = tf.keras.models.load_model('Alzheimers-disease-detection-main/my_model.h5')
except Exception as e:
    st.error(f"Model failed to load: {e}")
    model = None

# Sidebar Navigation
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Alzheimer Detection", "About Us"],
                           icons=["house", "activity", "info-circle"], menu_icon="cast", default_index=0)

# Home Page
if selected == "Home":
    def app():
        set_background("Alzheimers-disease-detection-main/images/bg7.jpg")
        st.title("🧠 AI Brain-Watch: Catching Alzheimer's Early!")
        st.write("""
            Welcome to our Alzheimer's Detection App!
            
            Upload an MRI brain image and let our AI model assist with detection. 
            This tool is meant to support early identification of Alzheimer’s stages using deep learning.
        """)
    app()

# Alzheimer Detection Page
elif selected == "Alzheimer Detection":
    def app():
        st.title("🔍 Alzheimer’s MRI Detection")
        uploaded_file = st.file_uploader("Upload an MRI scan (JPG/PNG):", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded MRI", use_column_width=True)

            # Preprocess
            img = image.resize((128, 128))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            if model:
                prediction = model.predict(img_array)
                classes = ['Mild Demented', 'Moderate Demented', 'Non Demented', 'Very Mild Demented']
                predicted_class = classes[np.argmax(prediction)]
                st.success(f"🧪 Prediction: **{predicted_class}**")
            else:
                st.error("Model not available for prediction.")
    app()

# About Us Page
elif selected == "About Us":
    def app():
        st.title("📘 About Us")
        st.write("""
        This project is developed to aid early-stage Alzheimer’s detection using Convolutional Neural Networks on MRI scans.

        Built with ❤️ by a team of passionate AI & healthcare enthusiasts.
        """)
    app()
