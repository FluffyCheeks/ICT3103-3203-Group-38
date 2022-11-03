from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import bcrypt  # added this 25 Oct 2022 (fumin) for hashing password

from luna.models import *
from luna.validator import *

# For duplicate email error
from django.db import IntegrityError


# Add this on 10 Oct 22, 12:34AM (fumin)
# Modified this on 15 Oct 22, 10:25PM (fumin)
def registration(request):
    if request.method == 'POST':
        while registration_validation(request, request.POST.get('first_name'), request.POST.get('last_name'),
                                      request.POST.get('email'),
                                      request.POST.get('allergies'), request.POST.get('password'),
                                      request.POST.get('confirm_password')):

            if request.POST.get('signup', '') == 'signup_confirm':
                # hash password done here before uploading to database
                normal_password = request.POST.get('password')
                bytePwd = normal_password.encode('utf-8')
                bcrypt_salt = bcrypt.gensalt()
                bcrypt_hash = bcrypt.hashpw(bytePwd, bcrypt_salt)

<<<<<<< Updated upstream
                urunler = Users.objects.create(role_id_id=1, first_name=request.POST.get('first_name'),
                                               last_name=request.POST.get('last_name'),
                                               email=request.POST.get('email'),
                                               #address = None,
                                               #phone = None,
                                               allergies=request.POST.get('allergies'),
                                               password=bcrypt_hash)
                urunler.save()
                print(bcrypt.checkpw(bytePwd, bcrypt_hash))  # if true means match
                return HttpResponseRedirect(request.path_info)
    return render(request, 'registration.html')
=======
                try:
                    urunler = Users.objects.create(role_id_id=1, first_name=request.POST.get('first_name'),
                                                   last_name=request.POST.get('last_name'),
                                                   email=request.POST.get('email'),
                                                   allergies=request.POST.get('allergies'),
                                                   password=bcrypt_hash)


                except IntegrityError as DuplicateEmailError:
                    messages.error(request, 'Registration Unsuccessful')
                    return render(request, "duplicate_email_error.html")

                urunler.save()  # save to database
                messages.success(request, 'Registration Successful')
                messages.success(request,'Check your email which you registered with -> check the inbox for the OTP sent to you to verify your email. Note: Check your spam folder.')

                return redirect('registration_success', request.POST.get('email'))

    return render(request, 'registration.html')
>>>>>>> Stashed changes
