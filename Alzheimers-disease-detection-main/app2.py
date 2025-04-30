import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import re
import base64
from fpdf import FPDF
import mysql.connector

# Database connection
try:
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="admin123",
        database="Alzheimers"
    )
    mycursor = mydb.cursor()
    print("Database connection successful")
except mysql.connector.Error as err:
    st.error(f"Error connecting to database: {err}")

# Styling
st.markdown("""
<style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
</style>""", unsafe_allow_html=True)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/png;base64,{bin_str}");
            background-position: center;
            background-size: cover;
            color: white;
        }}
        </style>
        """, unsafe_allow_html=True)

set_background('Alzheimers-disease-detection-main/images/bg7.jpg')

# Load model
model = tf.keras.models.load_model('Alzheimers-disease-detection-main/my_model.h5')
class_labels = ['Mild Demented', 'Moderate Demented', 'Non Demented', 'Very Mild Demented']

# Image preprocessing
def preprocess_image(image):
    image = image.convert('RGB')
    image = image.resize((176, 176))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Validations
def validate_phone_number(phone_number):
    return re.match(r'^\d{10}$', str(phone_number)) is not None

def validate_name(name):
    return all(char.isalpha() or char.isspace() for char in name)

def validate_input(name, age, contact, file):
    if not name or not validate_name(name):
        st.error("Invalid name. No numbers/special characters.")
        return False
    if not age:
        st.error("Please enter age.")
        return False
    if not validate_phone_number(contact):
        st.error("Phone number must be 10 digits.")
        return False
    if not file:
        st.error("Please upload an MRI scan.")
        return False
    return True

# Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Alzhiemer Detection", "About US"],
    icons=["house", "activity", "info-circle"],
    default_index=0,
    orientation="horizontal"
)

# Home Page
if selected == 'Home':
    st.title("🧠 Welcome to AI Brain-Watch")
    st.subheader("Your AI Companion for Early Alzheimer’s Detection")
    st.markdown("""
        Alzheimer's disease is the most common form of dementia. Early detection is crucial.

        With AI Brain-Watch, upload your MRI scan to check cognitive health:

        - 🟢 Non-Demented
        - 🟡 Very Mild Demented
        - 🟠 Mild Demented
        - 🔴 Moderate Demented

        Get insights in seconds.
    """)

# About Page
if selected == 'About US':
    st.title("About Us")
    st.markdown("""
        **AI Brain-Watch** helps detect Alzheimer's through MRI using AI.

        - 🔬 Uses CNN-based deep learning.
        - 🚀 Fast and accessible anywhere.
        - 🤖 Developed by Abhinav K as a solo AI/ML project.

        I hope this tool aids early intervention and better care.
    """)

# Alzheimer Detection Page
if selected == 'Alzhiemer Detection':
    st.title("🧪 Alzheimer Detection Web App")
    st.write("Fill the details and upload an MRI scan:")

    with st.form(key='detection_form'):
        name = st.text_input('Patient Name')
        age = st.number_input('Age', min_value=1, max_value=120, value=40)
        gender = st.radio('Gender', ['Male', 'Female', 'Other'])
        contact = st.text_input('Phone Number')
        file = st.file_uploader("Upload Brain MRI Scan", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Predict")

        if submit:
            if validate_input(name, age, contact, file):
                try:
                    img = Image.open(file)
                    processed = preprocess_image(img)
                    prediction = model.predict(processed)
                    result = class_labels[np.argmax(prediction)]

                    st.success(f"Prediction: {result}")

                    # Save result in DB
                    sql = "INSERT INTO records (name, age, gender, contact, prediction) VALUES (%s, %s, %s, %s, %s)"
                    val = (name, age, gender, contact, result)
                    mycursor.execute(sql, val)
                    mydb.commit()

                    # Optional: Downloadable PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=14)
                    pdf.cell(200, 10, txt="AI Brain-Watch Alzheimer Report", ln=True, align='C')
                    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
                    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
                    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
                    pdf.cell(200, 10, txt=f"Contact: {contact}", ln=True)
                    pdf.cell(200, 10, txt=f"Prediction: {result}", ln=True)

                    pdf_output = f"{name}_alz_report.pdf"
                    pdf.output(pdf_output)

                    with open(pdf_output, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{pdf_output}">📄 Download Report</a>'
                        st.markdown(href, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Prediction failed: {e}")
