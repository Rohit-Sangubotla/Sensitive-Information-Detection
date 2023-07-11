import streamlit as st
import easyocr
import cv2
import re
from matplotlib import pyplot as plt
import numpy as np

class CreditCard:
    def isValid(num):
        sum = CreditCard.doubleAndAdd(num) + CreditCard.addOdd(num)
        if(sum%10==0) and (CreditCard.size(num)>=13 and CreditCard.size(num)<=16) and CreditCard.prefix(num):
            return True
        else: return False
    
    def prefix(num):
        num=str(num)
        if(num[0]=='4' or num[0]=='5' or num[0]=='6' or num[0:2]=='37'):
            return True
        else: return False

    def size(num):
        num = str(num)
        return len(num)
    
    def doubleAndAdd(num):
        num = str(num)
        sum = 0
        if(CreditCard.size(num)%2==0): i = 0
        else: i = 1
        while(i<len(num)):
            sum+=CreditCard.digit(int(num[i])*2)
            i+=2
        return sum

    def digit(num):
        num=int(num)
        if(num//10==0):
            return num
        else:
            num = str(num)
            sum = 0
            sum+=int(num[0]) + int(num[1])
            return sum
    
    def addOdd(num):
        num = str(num)
        sum = 0
        if(CreditCard.size(num)%2==0): i = 1
        else: i = 0
        while(i<len(num)):
            sum+=int(num[i])
            i+=2
        return sum

def Read_Image(img):
    reader=easyocr.Reader(['en'], gpu=True)
    results = reader.readtext(img)
    print(results)
    return Check(results)

def Check(results):
    coordinates_list = []
    for i in results:
        Phoneresult = Phone_test(i) 
        Landlineresult = Landline_test(i)
        IPresult = IP_test(i)
        Aadharresult = Aadhar_test(i)
        Panresult = Pan_test(i)
        Licenseresult = License_test(i)
        CCresult = CC_test(i)
        if (Phoneresult or Landlineresult or IPresult or Aadharresult or Licenseresult or Panresult or CCresult):
            coordinates_list.append(i[0])
    return coordinates_list


def Phone_test(a):
    pattern = re.compile(r"((?<!\d)(?<!\d)(\+91)?[ -]?\d\d\d[ -]?\d\d[ -]?\d[ -]?\d\d\d\d(?!\d))")
    test = pattern.search(a[1])
    if test!=None:
        print("phone")
        if 'Phone Number' not in typesOfInfo: typesOfInfo.append('Phone Number')
        return True
  
def Landline_test(a):
    pattern = re.compile(r"((?<!\d)\d\d\d[ -]?\d\d\d\d[ -]?\d\d\d\d(?!\d))")
    test = pattern.search(a[1])
    if test!=None:
        print("landline")
        if 'Landline Number' not in typesOfInfo: typesOfInfo.append('Landline Number')
        return True

def Pan_test(a):
    pattern =  re.compile(r"[A-Z]{5}\d{4}[A-Z]")
    test =  pattern.search(a[1])
    if test!=None:
        print("pan")
        if 'PAN Number' not in typesOfInfo: typesOfInfo.append('PAN Number')
        return True
    
def IP_test(a):
    pattern = re.compile(r"((?<!\d)(?!10\.)(?!192\.168\.)(?!172\.(1[6-9]|2[0-9]|3[0-1])\.)(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(?!\d))")
    test = pattern.search(a[1])
    if test!=None:
        print("IP")
        if 'IP Address' not in typesOfInfo: typesOfInfo.append('IP Address')
        return True

def Aadhar_test(a):
    pattern = re.compile(r"((\d\d\d\d[ ]?\d\d\d\d[ ]?\d\d\d\d(?!\d)))")
    test = pattern.search(a[1])
    if test!=None and not CC_test:
        print("aadhar")
        if 'Aadhar Number' not in typesOfInfo: typesOfInfo.append('Aadhar Number')
        return True

def License_test(a):
    pattern = re.compile(r"(((AP|AR|AS|BR|CG|DL|GA|GJ|HR|HP|JK|JH|KA|KL|LD|MP|MH|ML|MZ|NL|OD|OR|PY|PB|RJ|SK|TN|TS|TR|UP|UK|UA|WB|AN|CH|DN|DD|LA|OT) ?\d\d ?\w\w ?\d\d\d\d))")
    test = pattern.search(a[1])
    if test!=None:
        print("Lic")
        if 'Vehicle Registration Number' not in typesOfInfo: typesOfInfo.append('Vehicle Registration Number')
        return True

def CC_test(a):
    pattern1 = re.compile(r"[Vv][Ii][Ss][Aa]")
    pattern2 = re.compile(r"\d\d/\d\d")
    pattern3 = re.compile(r"[Mm][Aa][Ss][Tt][Ee][Rr] ?[Cc][aA][rR][dD]")
    if pattern1.search(a[1])!=None:
        CCresult = True
    else:
        if pattern2.search(a[1])!=None:
            CCresult = True
        else:
            if pattern3.search(a[1])!=None:
                CCresult = True
            else:
                x = a[1].replace("-","")
                x = x.replace(" ","")
                if x.isdigit():
                    CCresult = CreditCard.isValid(x)
                    
                else:
                    CCresult =  False
    if CCresult:
        print("CC")
        if 'Credit Card Number' not in typesOfInfo: typesOfInfo.append('Credit Card Number')
    return CCresult

typesOfInfo=[]
title = """
    <p style="text-align:center; font-size:300%;margin-bottom:0px">
    <b>
    Sensitive information detector
    </b>
    </p>
"""
st.markdown(title, unsafe_allow_html=True)
center = """
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
st.markdown(center , unsafe_allow_html=True)


#st.image(img.read())
#st.image(img,caption = 'ur mom mmm')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
Found = False
file = st.file_uploader("input image here:", type = ['png','jpg','jpeg'])

if file:
    st.markdown('''
        <style>
            .uploadedFile {display: none}
        <style>''',
        unsafe_allow_html=True)
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 1)
    coordinates_list = Read_Image(img)
    if coordinates_list!=[]:
        Found = True
    for i in coordinates_list:
        cv2.rectangle(img, [int(i[0][0]),int(i[0][1])],[int(i[2][0]),int(i[2][1])],(255,0,0),3)

    st.image(img)
    text = """
        Image seems to contain the following sensitive information:
    """
    st.text(text)
    for x in typesOfInfo:
        st.text("• "+x)

