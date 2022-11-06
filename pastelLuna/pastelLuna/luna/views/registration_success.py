from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# from django.utils.html import escape

#Sending email and for OTP 
import smtplib
import pyotp

from luna.models import *
from luna.validator import *
from luna.views.registration import *
from luna.error_list import *



# Add this on 10 Oct 22, 12:34AM (fumin)
# Modified this on 15 Oct 22, 10:25PM (fumin)


def generate_totp(email):
    # Email Validation (Added on 01 Nov 22, 7:31PM, Fumin)
    global totp 
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

    return totp



def registration_success(request, email):
    if request.method != 'POST':
        generate_totp(email) # sent email out with OTP


    if request.method == 'POST':
        if request.POST.get('otp', '') == 'otp_confirm':
            while otp_check_sanitize(request, request.POST.get('otp_key')):
                otp_input = request.POST.get('otp_key')
                getTOTP = totp
                status = getTOTP.verify(otp_input)  # should return true if user is able to enter and submit OTP from email, within 2mins
                if status == True:
                    Users.objects.filter(email=email).update(email_valid=1)
                    messages.info(request, 'OTP is correct! Your email is now verified')
                    return redirect("home")
                else:
                    messages.error(request, 'OTP is wrong') 
                    return render(request, 'registration_success.html')

        if request.POST.get('otp_resub', '') == 'otp_resubmit':
            generate_totp(email)
            messages.info(request, 'OTP Resent! Check your email again')

    return render(request, 'registration_success.html')





