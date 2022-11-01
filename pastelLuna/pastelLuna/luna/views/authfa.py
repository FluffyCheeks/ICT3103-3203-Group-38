import random as rand
from django.shortcuts import redirect, render
from django.contrib.sessions import base_session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import hashlib 
import hmac 
import math 
import time
import base64
import re
from luna.models import *
from luna.validator import *
from django.utils.translation import gettext_lazy as _


def viewauth (request):
     sessionuser = request.session['id']
     context = {'profileorder':sessionuser}
     return render(request, "authfa.html", context)
     
#Validation #UserDATAFIELD
def clean_inputfield(self):
    special_char=re.compile('[@_!$%^&*()<>?/\|}{~:]')
    if special_char.search(self) == None:
            return True
    return False


@sensitive_post_parameters()
def checktoken (request):
     if request.method == 'POST':
          sessionuser = request.session['id']
          #sessionid = request.session['id']
          getcurrentuser = Users.objects.get(id=sessionuser)
          #tokenid = getcurrentuser.phone
          tokenid = getcurrentuser.email
          returntoken = generateTOTP(tokenid)
          inputtoek = request.POST.get('token')
          if (clean_inputfield(inputtoek) == 1):
               if (inputtoek == returntoken):
                    return redirect('/luna/checkout')
               else:
                    messages.success(request, 'Invalid Token!!!!!')
                    return redirect('/luna/viewauth')
          else:
               messages.success(request, 'Invalid Token!!!!!')
               return redirect('/luna/viewauth')
     else:
          return redirect('/luna/viewauth')

def generateTOTP(tokenid):
     length = 6
     step_in_seconds = 30 
     # randon key
     strtokenid = str(tokenid)
     randomstr = b"123123123djwkdhawjdk" 
     salt = bytes(strtokenid, 'utf8')

     key = b"".join([randomstr, salt])

     token = base64.b32encode(key)
     token.decode("utf-8")
     #print(token.decode("utf-8"))

     t = math.floor(time.time() // step_in_seconds)

     hmac_object = hmac.new(key, t.to_bytes(length=8, byteorder="big"), hashlib.sha1)
     hmac_sha1 = hmac_object.hexdigest()

     # truncate to 6 digits
     offset = int(hmac_sha1[-1], 16)
     binary = int(hmac_sha1[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
     totp = str(binary)[-length:]
     print(totp)
     return totp
