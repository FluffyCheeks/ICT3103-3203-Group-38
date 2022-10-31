from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import bcrypt #added this 25 Oct 2022 (fumin) for hashing password

from luna.models import *
from luna.validator import *
import base64

#from urllib.error import HTTPError  #for catching error when the duplicate email happens

def generatekey(tokenid):
   
     # randon key
     strtokenid = str(tokenid)
     randomstr = b"123123123djwkdhawjdk" 
     salt = bytes(strtokenid, 'utf8')

     key = b"".join([randomstr, salt])

     token = base64.b32encode(key)
     key = token.decode("utf-8")
     #print(token.decode("utf-8"))
     return key




# Add this on 10 Oct 22, 12:34AM (fumin)
# Modified this on 15 Oct 22, 10:25PM (fumin)
def registration(request):
    if request.method == 'POST':

        while registration_validation(request, request.POST.get('first_name'), request.POST.get('last_name'),
                                      request.POST.get('allergies'), request.POST.get('password'),
                                      request.POST.get('confirm_password')):

            if request.POST.get('signup', '') == 'signup_confirm':
                # hash password done here before uploading to database
                normal_password = request.POST.get('password')
                bytePwd = normal_password.encode('utf-8')
                bcrypt_salt = bcrypt.gensalt()
                bcrypt_hash = bcrypt.hashpw(bytePwd, bcrypt_salt)

                urunler = Users.objects.create(role_id_id=1, first_name=request.POST.get('first_name'),
                                               last_name=request.POST.get('last_name'),
                                               email=request.POST.get('email'),
                                               address = None,
                                               phone = None,
                                               allergies=request.POST.get('allergies'),
                                               password=bcrypt_hash)
                urunler.save()
                email = request.POST.get('email')
                returnsecret = str(generatekey(email))
                print(bcrypt.checkpw(bytePwd, bcrypt_hash))  # if true means match
                messages.success(request, "Please open the application and add an account in Microsoft Authenticator, This code will only show one time please do asap:" + returnsecret)
                return HttpResponseRedirect(request.path_info)

    return render(request, 'registration.html')
