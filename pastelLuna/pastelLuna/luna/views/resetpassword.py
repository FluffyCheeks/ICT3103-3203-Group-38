from luna.models import *
from password_generator import PasswordGenerator
import bcrypt, smtplib
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_variables
from django.utils.html import escape


@sensitive_variables('email', 'newPassword', 'bcrypt_salt')
def resetpassword(request):
    if request.method == 'POST':

        email = escape(request.POST['email'])
        exist_username = Users.objects.filter(email=email).exists()

        print(exist_username)
        if exist_username:

            pwo = PasswordGenerator()

            pwo.minlen = 30
            pwo.maxlen = 30
            pwo.minuchars = 3
            pwo.minlchars = 3
            pwo.minnumbers = 3
            pwo.minschars = 3
            newPassword = pwo.generate()

            message = 'Subject: {}\n\n{}'.format("Your password for with PastelDeLuna have been reseted, please use the following as password: ", newPassword)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("pasteldelunaaa@gmail.com", "ablyzjtawrjubgre")
            s.sendmail('pasteldelunaaa@gmail.com',email,message)

            newPassword = newPassword.encode('utf-8')
            bcrypt_salt = bcrypt.gensalt()
            newPassword = bcrypt.hashpw(newPassword, bcrypt_salt)

            Users.objects.filter(email=email).update(password=newPassword)
            Users.objects.filter(email=email).update(attempt=0)

            return redirect("loginpage")

        else:
            return redirect("resetpassword")
    else:
        return render(request, "resetpassword.html")