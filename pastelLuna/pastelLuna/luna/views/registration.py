from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import bcrypt  # added this 25 Oct 2022 (fumin) for hashing password
from django.utils.html import escape # to esacpe SQL inj

from luna.models import *
from luna.validator import *
from luna.allergies import *
import base64

# For duplicate email error
from django.db import IntegrityError


# Add this on 10 Oct 22, 12:34AM (fumin)
# Modified this on 15 Oct 22, 10:25PM (fumin)
def registration(request):
    json_data_al = allergies_list()
    if request.method == 'POST':
        some_var_allergies = request.POST.getlist('allergy')
        joined_string_allergies = ", ".join(some_var_allergies)

        while registration_validation(request, request.POST.get('first_name'), request.POST.get('last_name'),
                                      request.POST.get('email'),
                                      escape(joined_string_allergies), request.POST.get('password'),
                                      request.POST.get('confirm_password')):

            if request.POST.get('signup', '') == 'signup_confirm':
                # hash password done here before uploading to database
                normal_password = request.POST.get('password')
                bytePwd = normal_password.encode('utf-8')
                bcrypt_salt = bcrypt.gensalt()
                bcrypt_hash = bcrypt.hashpw(bytePwd, bcrypt_salt)

                try:
                    urunler = Users.objects.create(role_id_id=1, first_name=request.POST.get('first_name'),
                                                   last_name=request.POST.get('last_name'),
                                                   email=request.POST.get('email'),
                                                   allergies=escape(joined_string_allergies),
                                                   password=bcrypt_hash)


                except IntegrityError as DuplicateEmailError:
                    messages.error(request, 'Registration Unsuccessful')
                    return render(request, "duplicate_email_error.html")

                urunler.save()  # save to database
                getemail = request.POST.get('email')
                id = Users.objects.filter(email = getemail)
                num = ""
                for c in str(id):
                    if c.isdigit():
                        num = num + c
                returnsecret = str(generatekey(getemail, num))
                messages.success(request, 'Registration Successful')
                messages.success(request,'Check your email which you registered with -> check the inbox for the OTP sent to you to verify your email. Note: Check your spam folder.')
                messages.info(request, "Pastel De Luna uses Microsoft Authenticator for secure payment. You will need to create a Microsoft Account to make payment in future. This is your secret key and will only be shown once: " + returnsecret )
                messages.info(request, "1. Download Microsoft Authenticator on your phone -> 2. Under Authenticator Tab, create 'Other' account. -> 3. Input the secret key ")
                return redirect('registration_success', escape(request.POST.get('email')))
    else:
        return render(request, 'registration.html', {'al': json_data_al['allergies']})
    return render(request, 'registration.html',{'al': json_data_al['allergies']})


def generatekey(getemail, num):
     # randon key
     strtokenemail = str(getemail)
     strtokenid = str(num)
     randomstr = b"123123123djwkdhawjdk" 
     salt = bytes(strtokenemail, 'utf8')
     salt2 = bytes(strtokenid, 'utf8')
     key = b"".join([randomstr, salt, salt2])

     token = base64.b32encode(key)
     key = token.decode("utf-8")
     return key
