from luna.models import *
from password_generator import PasswordGenerator
import bcrypt, smtplib
from django.shortcuts import render, redirect


def resetpassword(request):
    if request.method == 'POST':

        email = request.POST['email']
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

            return render(request, "loginpage.html")

        else:
            msg = "Email not found"
            return render(request, "resetpassword.html")
    else:
        return render(request, "resetpassword.html")