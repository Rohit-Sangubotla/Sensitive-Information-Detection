import streamlit as st
import easyocr
import cv2
import re
from matplotlib import pyplot as plt
import numpy as np

class CreditCard:
    @staticmethod
    def main(number):
        if CreditCard.isValid(number):
            return True
        else: 
            return False
    @staticmethod
    def isValid(number):
        return (CreditCard.getSize(number) >= 13 and CreditCard.getSize(number) <= 16) and (CreditCard.prefixMatched(number, 4) or CreditCard.prefixMatched(number, 5) or CreditCard.prefixMatched(number, 37) or CreditCard.prefixMatched(number, 6)) and ((CreditCard.sumOfDoubleEvenPlace(number) + CreditCard.sumOfOddPlace(number)) % 10 == 0)
    @staticmethod
    def sumOfDoubleEvenPlace(number):
        sum = 0
        num = str(number) + ""
        i = CreditCard.getSize(number) - 2
        while (i >= 0):
            sum += CreditCard.getDigit(int(str(num[i]) + "") * 2)
            i -= 2
        return sum
    @staticmethod
    def getDigit(number):
        if (number < 9):
            return number
        return int(number / 10) + number % 10
    @staticmethod
    def sumOfOddPlace(number):
        sum = 0
        num = str(number) + ""
        i = CreditCard.getSize(number) - 1
        while (i >= 0):
            sum += int(str(num[i]) + "")
            i -= 2
        return sum
    @staticmethod
    def prefixMatched(number,  d):
        return CreditCard.getPrefix(number, CreditCard.getSize(d)) == d
    @staticmethod
    def getSize(d):
        num = str(d) + ""
        return len(num)
    @staticmethod
    def getPrefix(number,  k):
        if (CreditCard.getSize(number) > k):
            num = str(number) + ""
            return int(num[0:k])
        return number

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
    pattern1 =  re.compile(r"[A-Z]{5}\d{4}[A-Z]")
    pattern2 = re.compile(r"GOVT.? ?OF ? INDIA")
    pattern3 = re.compile(r"INCOME TAX DEPARTMENT")

    if pattern1.search(a[1])!=None:
        Panresult = True
    else:
        if pattern2.search(a[1])!=None:
            Panresult = True
        else:
            if pattern3.search(a[1])!=None:
                Panresult = True
            else:
                 Panresult =  False
    if Panresult:
        print("Pan")
        if 'Pan Card' not in typesOfInfo: typesOfInfo.append('Pan Card')
    return Panresult
    
def IP_test(a):
    pattern1 = re.compile(r"((?<!\d)(?!10\.)(?!192\.168\.)(?!172\.(1[6-9]|2[0-9]|3[0-1])\.)(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(?!\d))")
    pattern2 = re.compile(r"IP address")
    if pattern1.search(a[1])!=None:
        IPresult = True
    else:
        if pattern2.search(a[1])!=None:
            IPresult = True
        else: 
            IPresult = False
    if IPresult:
        print("IP")
        if 'IP Address' not in typesOfInfo: typesOfInfo.append('IP Address')
        return True

def Aadhar_test(a):
    pattern = re.compile(r"((\d\d\d\d[ ]?\d\d\d\d[ ]?\d\d\d\d(?!\d)))")
    test = pattern.search(a[1])
    if test!=None:
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
                    CCresult = CreditCard.main(x)
                    
                else:
                    CCresult =  False
    if CCresult:
        print("CC")
        if 'Credit Card Number' not in typesOfInfo: typesOfInfo.append('Credit Card Number')
    return CCresult

#Text
typesOfInfo=[]
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
personal privacy, secure online transactions, prevent identity theft and many other purposes.</p>''', unsafe_allow_html=True)

#Hiding the watermark
hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#Image uploader
Found = False
file = st.file_uploader("Upload your images here to check for sensitive information!", type = ['png','jpg','jpeg'])

#When the file is uploaded
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
        Image seems to contain one or more of the following sensitive information:
    """
    st.markdown(text, unsafe_allow_html=True)
    for x in typesOfInfo:
        textx = "• "+x
        st.markdown(textx, unsafe_allow_html=True)