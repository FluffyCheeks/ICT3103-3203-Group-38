from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

#Sending email and for OTP 
import smtplib
import pyotp

from luna.models import *
from luna.validator import *
from luna.views.registration import *
from luna.error_list import *

# Add this on 10 Oct 22, 12:34AM (fumin)
# Modified this on 15 Oct 22, 10:25PM (fumin)
print("REGISTRATION_SUCCESS.PY VIEW IS USED")



def generate_totp(email):
    # Email Validation (Added on 01 Nov 22, 7:31PM, Fumin)
    global totp  # Not sure if still need this 'global' now, since Yuhui change it to here.. dont have to global anymore (03 Nov, Fumin)
    emailtosent = email 
    randombase = pyotp.random_base32()
    totp = pyotp.TOTP(randombase, interval=120)  # expire after 2mins, recommended by google
    OTPsent = totp.now() #this will generate the 6 Digits
    otp = OTPsent + "  is your OTP. Enter the OTP to activate your account. OTP expires in 2 minutes"
    message = 'Subject: {}\n\n{}'.format("Thank you for registering with PastelDeLuna", otp)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("pasteldelunaaa@gmail.com", "ablyzjtawrjubgre")
    s.sendmail('pasteldelunaaa@gmail.com', emailtosent, message)
    # print(totp.now())

    return totp

def registration_success(request, email):
    # print("fails here", email)
    if request.method != 'POST':
        print("Email is sent out to user! ")
        generate_totp(email)

    print("kan dao wo ma")

    if request.method == 'POST':
        # print("it comes here")
        if request.POST.get('otp', '') == 'otp_confirm':
            print("IT CAME HERE!")
            while otp_check_sanitize(request, request.POST.get('otp_key')):
                otp_input = request.POST.get('otp_key')
                print("otp_input:" + otp_input)
                getTOTP = totp
                status = getTOTP.verify(otp_input)  # should return true if user is able to enter and submit OTP from email, within 2mins
                print("STATUS:" , status)
                if status == True:
                    print("OTP MATCHES!!!")
                    #
                    # TO DO
                    #   filter by email, then update the email_valid field from 0 to 1
                    return redirect("home")
                else:
                    #messages.error('FAIL OTP, INCORRECT') -> this err msg like cannot work lei
                    print("hommeeeee sweet homeeeeee")
                    return redirect("home")

    print("yes can dao ni")
    return render(request, 'registration_success.html')





