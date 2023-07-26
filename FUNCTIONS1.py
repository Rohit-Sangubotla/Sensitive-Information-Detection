#THIS FILE HAS THE FUNCTIONS

import re
import easyocr
import base64 
from PIL import Image
import numpy as np

typesOfInfo=[]
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

def Phone_test(a):
    pattern = re.compile(r"((?<!\d)(?<!\d)(\+91)?[ -]?\d\d\d[ -]?\d\d[ -]?\d[ -]?\d\d\d\d(?!\d))")
    test = pattern.search(a)
    if test!=None:
        return True
    else:
        return False
  
def Landline_test(a):
    pattern = re.compile(r"((?<!\d)\d\d\d[ -]?\d\d\d\d[ -]?\d\d\d\d(?!\d))")
    test = pattern.search(a)
    if test!=None:
        return True
    else:
        return False

def Pan_test(a):
    pattern1 =  re.compile(r"[A-Z]{5}\d{4}[A-Z]")
    pattern2 = re.compile(r"GOVT.? ?OF ? INDIA")
    pattern3 = re.compile(r"INCOME TAX DEPARTMENT")

    if pattern1.search(a)!=None:
        Panresult = True
    else:
        if pattern2.search(a)!=None:
            Panresult = True
        else:
            if pattern3.search(a)!=None:
                Panresult = True
            else:
                 Panresult =  False
    return Panresult
    
def IP_test(a):
    pattern1 = re.compile(r"((?<!\d)(?!10\.)(?!192\.168\.)(?!172\.(1[6-9]|2[0-9]|3[0-1])\.)(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(?!\d))")
    pattern2 = re.compile(r"IP address")
    if pattern1.search(a)!=None:
        IPresult = True
    else:
        if pattern2.search(a)!=None:
            IPresult = True
        else: 
            IPresult = False
    return IPresult

def Aadhar_test(a):
    pattern = re.compile(r"((\d\d\d\d[ ]?\d\d\d\d[ ]?\d\d\d\d(?!\d)))")
    test = pattern.search(a)
    if test!=None:
        return True
    else:
        return False

def License_test(a):
    pattern = re.compile(r"(((AP|AR|AS|BR|CG|DL|GA|GJ|HR|HP|JK|JH|KA|KL|LD|MP|MH|ML|MZ|NL|OD|OR|PY|PB|RJ|SK|TN|TS|TR|UP|UK|UA|WB|AN|CH|DN|DD|LA|OT) ?\d\d ?\w\w ?\d\d\d\d))")
    test = pattern.search(a)
    if test!=None:
        return True
    else:
        return False

def CC_test(a):
    pattern1 = re.compile(r"[Vv][Ii][Ss][Aa]")
    pattern2 = re.compile(r"\d\d/\d\d")
    pattern3 = re.compile(r"[Mm][Aa][Ss][Tt][Ee][Rr] ?[Cc][aA][rR][dD]")
    if pattern1.search(a)!=None:
        CCresult = True
    else:
        if pattern2.search(a)!=None:
            CCresult = True
        else:
            if pattern3.search(a)!=None:
                CCresult = True
            else:
                x = a.replace("-","")
                x = x.replace(" ","")
                if x.isdigit():
                    CCresult = CreditCard.isValid(x)
                    
                else:
                    CCresult =  False
    return CCresult



