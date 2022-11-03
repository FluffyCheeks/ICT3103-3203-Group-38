
import decimal
import random as rand

from cryptography.fernet import Fernet
from django.shortcuts import redirect, render

from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.html import escape
from luna.models import *
from luna.validator import *
import re

from datetime import datetime    
import pytz

from django.utils.translation import gettext_lazy as _
import hashlib 
import hmac 
import math 
import time
import base64


@xframe_options_deny
@sensitive_variables()
def checkout (request):
    uid = request.session['id']
    profileorder = Users.objects.select_related("role_id").filter(id=uid)
    rawcart = Cart.objects.select_related("user_id").filter(user_id=uid)
    
   
    for item in rawcart:
        if item.quantity > item.product_id.stock_available:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.select_related("user_id").filter(user_id=uid)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.total_price * item.quantity
    
    context = {'cartitems':cartitems, 'total_price':total_price, 'rawcart':rawcart, 'profileorder':profileorder}
    return render(request, "checkout.html", context)


def validate_credit_card(cardnumber):
    if len(cardnumber) == 16:
            for i in range(0, len(cardnumber)):
                cardnumber[i] = int(cardnumber[i])
            last = cardnumber[15]
            first = cardnumber[:15]
            first = first[::-1]
            
            for i in range(len(first)):
                if i % 2 == 0:
                    first[i] = first[i] * 2
                if first[i] > 9:
                    first[i] -= 9
            sum_all = sum(first)
        
            t1 = sum_all % 10
            t2 = t1 + last
            if t2 % 10 == 0:
                return True
            else:
                return False         
    else:
        return False   
        

def mask_cc_number(cc_string, digits_to_keep=4, mask_char='*'):
   cc_string_total = sum(map(str.isdigit, cc_string))

   if digits_to_keep >= cc_string_total:
       print("Not enough numbers. Add 10 or more numbers to the credit card number.")

   digits_to_mask = cc_string_total - digits_to_keep
   masked_cc_string = re.sub('\d', mask_char, cc_string, digits_to_mask)

   return masked_cc_string

#Validation #UserDATAFIELD
def clean_inputfield(self):
    special_char=re.compile('[@_!$%^&*()<>?/\|}{~:]')
    if special_char.search(self) == None:
            return True
    return False

def clean_Phoneno(self):
    special_char=re.compile('[@_!$%^&*()<>?/\|}{~:]#')
    if special_char.search(self) == None:
        if (self.isdigit() and len(self) == 8):
            return True
    return False

def clean_emailaddress(self):
    special_char=re.compile('[!$%^&*()<>?/\|}{~:]')
    if special_char.search(self) == None:
            return True
    return False

def checktoken (token, email):
          #sessionid = request.session['id']
          inputtoek = token
          returntoken = generateTOTP(email)
          if (clean_inputfield(inputtoek) == 1):
               if (inputtoek == returntoken):
                    return True
               else:                  
                    return False
          else:              
               return False
  

def generateTOTP(email):
     length = 6
     step_in_seconds = 30 
     # randon key
     strtokenid = str(email)
     randomstr = b"123123123djwkdhawjdk" 
     salt = bytes(strtokenid, 'utf8')

     key = b"".join([randomstr, salt])

     token = base64.b32encode(key)
     token.decode("utf-8")
     #print(token.decode("utf-8"))

     t = math.floor(time.time() // step_in_seconds)

     hmac_object = hmac.new(key, t.to_bytes(length=8, byteorder="big"), hashlib.sha1)
     hmac_sha1 = hmac_object.hexdigest()

     
     offset = int(hmac_sha1[-1], 16)
     binary = int(hmac_sha1[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
     totp = str(binary)[-length:]
     #print(totp)
     return totp


#@login_required(login_url='login')
@xframe_options_deny
@sensitive_post_parameters()
def placeorder (request):
    if request.method == 'POST' and 'payment_mode1' in request.POST:
        uid = request.session['id']
        cardnumber = escape(request.POST.get('creditCradNum'))
        fistn = escape(request.POST.get('fname'))
        lastn = escape(request.POST.get('lname'))
        disccode = escape(request.POST.get('disc'))
        phonenumber = escape(request.POST.get('Phoneno'))
        address = escape(request.POST.get('Addr'))
        email = escape(request.POST.get('email'))
        token = escape(request.POST.get('token'))
        sanitizeph = phonenumber
        list1 = list(cardnumber)
        if (clean_inputfield(cardnumber) and checktoken(token, email)) == 1:
            if (validate_credit_card(list1) and clean_Phoneno(sanitizeph) and clean_emailaddress(email) and clean_emailaddress(address) and clean_inputfield(fistn) and clean_inputfield(lastn) and clean_inputfield(disccode)) == 1:
                neworder = Orders()
                uid = request.session['id']
                neworder.first_name = escape(request.POST.get('fname'))
                neworder.last_name = escape(request.POST.get('lname'))
                neworder.email = escape(request.POST.get('email'))
                neworder.phone = escape(request.POST.get('Phoneno'))
                neworder.user = Users.objects.get(id=uid) 
                neworder.address =  escape(request.POST.get('Addr'))
                neworder.payment_mode = request.POST.get('payment_mode1')
                Masked = mask_cc_number(request.POST.get('creditCradNum'))
                key = Fernet.generate_key()
                fernet = Fernet(key)
                enccc = fernet.encrypt(Masked.encode())
                neworder.ccard_digits = enccc
                discode =  request.POST.get('disc')
                singapore = pytz.timezone('Asia/Singapore')
                now = datetime.now(singapore)
                neworder.orderDate = now

                cart = Cart.objects.select_related("user_id").filter(user_id=uid)
                cart_total_price = 0
                for item in cart:
                    cart_total_price = cart_total_price + item.total_price * item.quantity
            
                discountcode = "10OFF"
                if discode == discountcode:
                    neworder.total_price = cart_total_price - decimal.Decimal(float('10.00'))
                    if neworder.total_price < 0:
                        neworder.total_price = 0
                else:
                    neworder.total_price = cart_total_price

                trackno = 'sharma'+ str(rand.randint(1000000000, 9999999999))
                while Orders.objects.filter(tracking_no = trackno) is None:
                    trackno = 'sharma'+str(rand.randint(1000000000, 9999999999))

                neworder.tracking_no = trackno
                neworder.save()
                
                
                neworderItem = Cart.objects.select_related("user_id").filter(user_id=uid)
                for item in neworderItem:
                    OrderItem.objects.create(
                    order = neworder,
                    productID = item.product_id,
                    price = item.quantity * item.total_price,
                    quantity = item.quantity
                    )
                    #decrease product qty from names
                    string =str(item.product_id)     
                    prodID = string
                    orderproduct = Product_Details.objects.filter(name=prodID).first()
                    orderproduct.stock_available = orderproduct.stock_available - item.quantity
                    orderproduct.save()

                    
                # Cart.objects.filter(user=request.user).delete()
                Cart.objects.select_related("user_id").filter(user_id=uid).delete()
                messages.success(request, 'Order Success, Thank you for the order')
                return redirect('/luna/checkout')
            else:
                messages.success(request, 'Order Not success, Please enter a Valid credit card number, valid required field and token')
                return redirect('/luna/checkout')
        else:
            messages.success(request, 'Order Not success, Please enter a Valid credit card number, valid required field and token')
            return redirect('/luna/checkout')

    if request.method == 'POST' and 'payment_mode' in request.POST:
        fistn = escape(request.POST.get('fname'))
        lastn = escape(request.POST.get('lname'))
        disccode = escape(request.POST.get('disc'))
        phonenumber = escape(request.POST.get('Phoneno'))
        address = escape(request.POST.get('Addr'))
        email = escape(request.POST.get('email'))
        token = escape(request.POST.get('token'))
        sanitizeph = phonenumber
        if checktoken(token, email) == 1:
            if (clean_Phoneno(sanitizeph) and clean_emailaddress(email) and clean_emailaddress(address) and clean_inputfield(fistn) and clean_inputfield(lastn) and clean_inputfield(disccode)) == 1:
                neworder = Orders()
                uid = request.session['id']
                neworder.first_name = escape(request.POST.get('fname'))
                neworder.last_name = escape(request.POST.get('lname'))
                neworder.email = escape(request.POST.get('email'))
                neworder.phone = escape(request.POST.get('Phoneno'))
                neworder.user = Users.objects.get(id=uid) 
                neworder.address = escape(request.POST.get('Addr'))
                neworder.payment_mode = request.POST.get('payment_mode')
                discode = request.POST.get('disc')

                singapore = pytz.timezone('Asia/Singapore')
                now = datetime.now(singapore)
                neworder.orderDate = now

                cart = Cart.objects.select_related("user_id").filter(user_id=uid)
                cart_total_price = 0
                for item in cart:
                    cart_total_price = cart_total_price + item.total_price * item.quantity
            
                discountcode = "10OFF"
                if discode == discountcode:
                    neworder.total_price = cart_total_price - decimal.Decimal(float('10.00'))
                    if neworder.total_price < 0:
                        neworder.total_price = 0
                else:
                    neworder.total_price = cart_total_price

                trackno = 'sharma'+ str(rand.randint(1000000000, 9999999999))
                while Orders.objects.filter(tracking_no = trackno) is None:
                    trackno = 'sharma'+str(rand.randint(1000000000, 9999999999))

                neworder.tracking_no = trackno
                neworder.save()
                
                
                #neworderItem = Cart.objects.filter(user=request.user)
                neworderItem = Cart.objects.select_related("user_id").filter(user_id=uid)
                for item in neworderItem:
                    OrderItem.objects.create(
                    order = neworder,
                    productID = item.product_id,
                    price = item.quantity * item.total_price,
                    quantity = item.quantity
                    )
                    #decrease product qty from stock base on name
                    string =str(item.product_id)     
                    prodID = string
                    orderproduct = Product_Details.objects.filter(name=prodID).first()
                    orderproduct.stock_available = orderproduct.stock_available - item.quantity
                    orderproduct.save()

                    
                # Cart.objects.filter(user=request.user).delete()
                Cart.objects.select_related("user_id").filter(user_id=uid).delete()
                messages.success(request, 'Order Success, Thank you for the order')
                return redirect('/luna/checkout')

            else:
                messages.success(request, 'Order Not success, Please enter valid user required field or token')
                return redirect('/luna/checkout')

        else:
            messages.success(request, 'Order Not success, Please enter valid user required field or token')
            return redirect('/luna/checkout')
    else:
        messages.success(request, 'Order Not Success, Please re-order again')
        return redirect('/luna/checkout')



