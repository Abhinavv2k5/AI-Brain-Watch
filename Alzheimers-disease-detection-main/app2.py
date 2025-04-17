import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import re
import base64
from fpdf import FPDF

import mysql.connector

# Connect to the MySQL database
try:
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="admin123",
        database="Alzheimers"
    )
    print("Database connection successful")
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit(1)
# Get a cursor object to execute SQL queries
mycursor = mydb.cursor()




st.markdown("""
<style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
</style>""",
unsafe_allow_html=True)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/png;base64,{bin_str}");
        background-position: center;
        background-size: cover;
        color: white;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('Alzheimers-disease-detection-main\\images\\bg7.jpg')

# Load the saved model
model = tf.keras.models.load_model('Alzheimers-disease-detection-main\my_model.h5')

# Define the class labels
class_labels = ['Mild Demented', 'Moderate Demented',
                'Non Demented', 'Very Mild Demented']

# Define the function to preprocess the image


def preprocess_image(image):
    image = image.convert('RGB')
    image = image.resize((176, 176))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Define the Streamlit app

def validate_phone_number(phone_number):
    """
    Validates that a phone number is a 10-digit number.
    """
    pattern = r'^\d{10}$'
    contact=re.match(pattern, str(phone_number))
    if not contact:
        st.error('Please enter a 10 digit number!')
        return False
    return True

def validate_name(name):
    if not all(char.isalpha() or char.isspace() for char in name):
        st.error("Name should not contain numbers or special character.")
        return False
    return True

def validate_input(name, age,contact,file):
    if not name:
        st.error('Please enter the patients name!')
        return False
    if not age:
        st.error('Please enter your age!')
        return False
    if not contact:
        st.error('Please enter your contact number!')
        return False
    if not file:
        st.error('Please upload the MRi Scan!')
        return False
    return True
#with st.sidebar:
selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Alzhiemer Detection", "About US"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
if selected == 'Home':
    def app():
        st.title("🧠 Welcome to AI Brain-Watch")
        st.subheader("Your AI Companion for Early Alzheimer’s Detection")
        
        st.write("""
        Alzheimer's disease is the most common form of dementia, progressively affecting memory, thinking, and behavior.
        Early detection is crucial for effective care and management.
        
        With AI Brain-Watch, simply upload your brain MRI scan and let our intelligent system analyze it for signs of Alzheimer’s.
        Our model classifies scans into four distinct stages of cognitive health:
        """)

        st.write("🟢 **Non-Demented**")
        st.write("🟡 **Very Mild Demented**")
        st.write("🟠 **Mild Demented**")
        st.write("🔴 **Moderate Demented**")

        st.write("""
        Let’s take a step towards proactive brain health.
        Try it now and get insights in seconds.
        """)


if selected == 'About US':
    def app():
        st.title("About Us")
        
        st.subheader("AI Brain-Watch: Revolutionizing Alzheimer’s Detection")

        st.write("""
        Alzheimer's disease is one of the most challenging health conditions in the world. With its growing prevalence, early detection is crucial for timely intervention and better quality of life. Traditional methods like MRI scans can be expensive, time-consuming, and often require a specialist's opinion. 
        This is where **AI Brain-Watch** steps in—an innovative, easy-to-use web application that allows you to assess the presence of Alzheimer’s disease using just an MRI scan. 

        **AI Brain-Watch** leverages cutting-edge deep learning techniques to accurately detect signs of Alzheimer’s across all stages of the disease, offering a faster, portable, and more accessible solution for early detection.
        """)

        st.write("""
        ### How AI Brain-Watch Works:
        By uploading your brain MRI scan to this platform, our sophisticated Convolutional Neural Network (CNN) model will analyze the image and classify it into one of the following stages:
        
        🟢 **Non-Demented** – No signs of Alzheimer’s detected.
        
        🟡 **Very Mild Demented** – Initial signs of Alzheimer’s present.
        
        🟠 **Mild Demented** – Moderate cognitive impairment detected.
        
        🔴 **Moderate Demented** – Severe cognitive impairment detected.
        
        This fast and intuitive process takes seconds, allowing users to get an instant report without the need for a traditional medical facility visit.
        """)

        st.write("""
        ### My Mission:
        My mission with **AI Brain-Watch** is to make Alzheimer’s detection easier, faster, and more accessible to people of all ages. I aim to empower individuals by providing them with immediate insights into their cognitive health, allowing for early intervention and improved management of the condition.

        I understand the importance of brain health and the impact of Alzheimer’s disease on both individuals and their families. With this application, I hope to provide a tool that makes early detection a reality for everyone, no matter where they are.
        """)

        st.write("""
        ### Behind the Project:
        **AI Brain-Watch** is a solo project created and developed by **Abhinav K**, a passionate AI enthusiast dedicated to building impactful healthcare solutions through technology.

        From data preprocessing to model training and frontend development, every part of this application has been thoughtfully designed and implemented to ensure reliability, ease of use, and real-world value.
        """)

        st.write("""
        ### Why Choose AI Brain-Watch?
        - **Portable and Convenient**: Unlike traditional methods, you can use this web app anytime, anywhere, without needing to visit a hospital.
        - **Fast Results**: Get your Alzheimer’s diagnosis in seconds, not hours or days.
        - **Accessible to All**: The app is user-friendly and accessible across devices, ensuring that anyone, regardless of age or technical ability, can use it.
        - **AI-Powered**: Built with advanced CNN algorithms for accurate and reliable results.

        I hope that this app helps individuals around the world detect Alzheimer’s disease at an early stage, enabling them to take proactive steps towards managing their health.
        """)

        st.write("""
        Thank you for choosing **AI Brain-Watch**. Together, we can take a step toward proactive brain health.
        """)



if selected=='Alzhiemer Detection':
  def app():
    st.title('Alzheimer Detection Web App')
    st.write('Please enter your personal details along with MRI scan.')

    # Add fields for name, age, contact, and gender
    with st.form(key='myform', clear_on_submit=True):
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=1, max_value=150, value=40)
        gender = st.radio('Gender', ('Male', 'Female','Other'))
        contact = st.text_input('Contact Number', value='', key='contact')

        file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
        submit=st.form_submit_button("Submit")

        # Define a function to insert the form data into the `prediction` table
    def insert_data(name, age, gender, contact, prediction):
        try:
          sql = "INSERT INTO predictions (Patient_Name, Age, Gender, Contact, Prediction) VALUES (%s, %s, %s, %s, %s)"
          val = (name, age, gender, contact, prediction)
          mycursor.execute(sql, val)
          mydb.commit()
          print(mycursor.rowcount, "record inserted")
        except mysql.connector.Error as err:
          print("Error inserting record:", err)  

                
    if file is not None and validate_input(name, age,contact,file) and validate_phone_number(contact) and validate_name(name):
                  st.success('Your personal information has been recorded.', icon="✅")
                  image = Image.open(file)
                  png_image = image.convert('RGBA')
                  st.image(image, caption='Uploaded Image', width=200)
                  # Use the fields for name, age, contact, and gender in the output
        
                  st.write('Name:', name)
                  st.write('Age:', age)
                  st.write('Gender:', gender)
                  st.write('Contact:', contact)
                  image = preprocess_image(image)
                  prediction = model.predict(image)
                  prediction = np.argmax(prediction, axis=1)
                  st.success('The predicted class is: '+ class_labels[prediction[0]])
                  result_str = 'Name: {}\nAge: {}\nGender: {}\nContact: {}\nPrediction for Alzheimer: {}'.format(
                     name, age, gender, contact, class_labels[prediction[0]])
                  insert_data(name, age, gender, contact, class_labels[prediction[0]])
                  export_as_pdf = st.button("Export Report")

                  def create_download_link(val, filename):
                    b64 = base64.b64encode(val)  # val looks like b'...'
                    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
        
                  if export_as_pdf:
                     pdf = FPDF()
                     pdf.add_page()
                     # set the border style
                     pdf.set_draw_color(0, 0, 0)
                     pdf.set_line_width(1)

                     # add a border to the entire page
                     pdf.rect(5.0, 5.0, 200.0, 287.0, 'D')
    
                     # Set font for title
                     pdf.set_font('Times', 'B', 24)
                     pdf.cell(200, 20, 'Alzheimer Detection Report', 0, 1, 'C')
    
                     # Set font for section headers
                     pdf.set_font('Arial', 'B', 16)
                     pdf.cell(200, 10, 'Patient Details', 0, 1)
    
                     # Set font for regular text
                     pdf.set_font('Arial', '', 12)
                     pdf.cell(200, 10, f'Name: {name}', 0, 1)
                     pdf.cell(200, 10, f'Age: {age}', 0, 1)
                     pdf.cell(200, 10, f'Gender: {gender}', 0, 1)
                     pdf.cell(200, 10, f'Contact: {contact}', 0, 1)
                     pdf.ln(0.15)
                     pdf.ln(0.15)



                     # Add the image to the PDF object's images dictionary
                     png_file = "image.png"
                     png_image.save(png_file, "PNG")
                     pdf.cell(200, 10, 'MRI scan:', 0, 1)
                     pdf.image(png_file, x=40, y=80, w=50,h=50)
                     pdf.ln(0.15)
                     pdf.ln(10.0)
                     pdf.ln(10.0)
                     pdf.ln(10.15)
                     pdf.ln(10.15)
                     pdf.ln(1.15)
                     pdf.ln(1.15)
                     pdf.ln(1.15)

                     # Set font for prediction text
                     pdf.set_font('Arial', 'B', 16)
                     pdf.cell(200, 10, f'Prediction for Alzheimer: {class_labels[prediction[0]]}', 0, 1)
                     pdf.ln(2.0)
                     pdf.set_font('Arial', 'B', 12)
                     if (prediction!=2):
                      pdf.set_text_color(255, 0, 0)
                      pdf.cell(200,10,'Demetia detected in your MRI, kindly consult a nearby neurologist immediately!',0,1)
                      pdf.set_text_color(0, 0, 255)
                      pdf.set_font('Arial', 'B', 10)
                      pdf.cell(200, 10, 'Here are some precautions you can take:', 0, 1, 'C')
                      pdf.ln(2)

                      precautions = [
                        '1. Stay mentally active: Engage in mentally stimulating activities such as reading, writing, puzzles, and games to keep your brain active.',
                        '2. Stay physically active: Exercise regularly to improve blood flow to the brain and help prevent cognitive decline.',
                        '3. Eat a healthy diet: Eat a balanced diet that is rich in fruits, vegetables, whole grains, and lean protein to help maintain brain health.',
                        '4. Stay socially active: Engage in social activities and maintain social connections to help prevent social isolation and depression.',
                        '5. Get enough sleep: Aim for 7-8 hours of sleep per night to help improve brain function and prevent cognitive decline.'                ]
        
                      pdf.set_font('Arial', '', 12)

                      for precaution in precautions:
                       pdf.multi_cell(190, 10, precaution, 0, 1, 'L')
                       pdf.ln(1)
          
                     else:
                       pdf.set_text_color(0, 0, 0)
                       pdf.cell(200,10,'Congratulations! There is no sign of demetia in your MRI.',0,1)
    
                      # Create and display the download link
                     html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")
                     st.markdown(html, unsafe_allow_html=True)





# Run the app
if __name__ == '__main__':
    app()