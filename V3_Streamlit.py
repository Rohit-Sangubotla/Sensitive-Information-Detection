#STREAMLIT
import cv2
from FUNCTIONS1 import * 
import streamlit as st
import numpy as np 
import base64
import requests
import json
from PIL import Image

def Read_Image(img):
    reader=easyocr.Reader(['en'],gpu=False)
    results = reader.readtext(img)
    return Check(results)

def Check(results):
    coordinates_list = []
    for i in results:
        s = i[1]
        inputs = {"i":s}
        Phoneresult = requests.post(url = "http://127.0.0.1:8000/PhoneNumber", data = json.dumps(inputs))
        Landlineresult = requests.post(url = "http://127.0.0.1:8000/Landline", data = json.dumps(inputs))
        IPresult = requests.post(url = "http://127.0.0.1:8000/IP", data = json.dumps(inputs))
        Aadharresult = requests.post(url = "http://127.0.0.1:8000/Aadhar", data = json.dumps(inputs))
        Panresult = requests.post(url = "http://127.0.0.1:8000/PAN", data = json.dumps(inputs))
        Licenseresult = requests.post(url = "http://127.0.0.1:8000/License", data = json.dumps(inputs))
        CCresult = requests.post(url = "http://127.0.0.1:8000/CreditCard", data = json.dumps(inputs))
        
        if (Phoneresult.text=="true" or Landlineresult.text=="true" or IPresult.text=="true" or Aadharresult.text=="true" or Licenseresult.text=="true" or Panresult.text=="true" or CCresult.text=="true"):
            coordinates_list.append(i[0])
        if Phoneresult.text=="true":
            if 'Phone Number' not in typesOfInfo: typesOfInfo.append('Phone Number')
        if Landlineresult.text=="true":
            if 'Landline Number' not in typesOfInfo: typesOfInfo.append('Landline Number')
        if Panresult.text=="true"=="true":
            if 'Pan Card' not in typesOfInfo: typesOfInfo.append('Pan Card')
        if IPresult.text=="true":
            if 'IP Address' not in typesOfInfo: typesOfInfo.append('IP Address')
        if Aadharresult.text=="true":
            if 'Aadhar Number' not in typesOfInfo: typesOfInfo.append('Aadhar Number')
        if Licenseresult.text=="true":
            if 'Vehicle Registration Number' not in typesOfInfo: typesOfInfo.append('Vehicle Registration Number')
        if CCresult.text=="true":
            if 'Credit Card Number' not in typesOfInfo: typesOfInfo.append('Credit Card Number')
    return [coordinates_list,typesOfInfo]

typesOfInfo=[]
#Text
title = """
    <p style="text-align:center; font-size:300%;margin-bottom:0px">
    <b>
    Sensitive information detector
    </b>
    </p>
"""
st.markdown(title, unsafe_allow_html=True)
subtitle = """
<p style = "text-align:center">
    <span style="color:blue;font-size:150%">
    Protecting 
    </span>
    <span style="color:white;font-size:150%">
    your 
    </span>
    <span style="color:red;font-size:150%">
    privacy 
    </span>
    <span style="color:white;font-size:150%">
    on the internet
    </span>
"""
st.markdown(subtitle , unsafe_allow_html=True)
st.markdown("""
<style>
.centerfont {
    font-family:"Times New Roman" !important;
    text-align:left;
    margin-bottom:0px;
    font-size:110%;
}
</style>
""", unsafe_allow_html=True)
st.markdown('''<p class="centerfont">With the increasing need for privacy protection online in mind, the Sensitive 
Information Detector is a great tool to help detect personally identifiable.
information that can compromise  security. This can be used to protect
personal privacy, secure online transactions, prevent identity theft and for    many other purposes.</p>''', unsafe_allow_html=True)

#Hiding the watermark
hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#Image uploader
Found = False
file = st.file_uploader("Upload your images here to check for sensitive information.", type = ['png','jpg','jpeg'])

#When the file is uploaded
if file:
    st.markdown('''
        <style>
            .uploadedFile {display: none}
        <style>''',
        unsafe_allow_html=True)
    
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 1)
    Result_list =  Read_Image(img)
    coordinates_list = Result_list[0]
    typesOfInfo = Result_list[1]
    if coordinates_list:
        Found = True
    print(coordinates_list)
    for i in coordinates_list:
        top_left = (i[0][0], i[0][1])
        bottom_right = (i[2][0], i[2][1])
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 3)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    st.image(img)
    
    text = """
        Image seems to contain one or more of the following sensitive information:
    """
    st.markdown(text, unsafe_allow_html=True)
    for x in typesOfInfo:
        textx = "• "+x
        st.markdown(textx, unsafe_allow_html=True)

#command: streamlit run V3_Streamlit.py
