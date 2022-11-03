from django.shortcuts import render, redirect
from luna.models import *
import bcrypt
import smtplib
from password_generator import PasswordGenerator


def loginpage(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        exist_username = Users.objects.filter(email=email).exists()

        password = password.encode('utf-8')

        dBPassword = Users.objects.get(email=email)
        dBPassword = dBPassword.password

        dBPassword = str(dBPassword).replace("b'", "").replace("'", "")
        dBPassword = dBPassword.encode('utf-8')

        if exist_username:

            someuser = Users.objects.get(email__contains=email)

            attempt = someuser.attempt + 1
            Users.objects.filter(id=someuser.id).update(attempt=attempt)

            if someuser.attempt < 6:
                if bcrypt.checkpw(password, dBPassword):
                    if someuser is not None:
                        Users.objects.filter(id=someuser.id).update(attempt=0)
                        cookie_session(request)
                        role_id = request.session['role_id_id']
                        if role_id == 1:
                            return redirect("home_aft_login")
                        elif role_id == 2:
                            return redirect("admin_dashboard")
                        elif role_id ==3:
                            return redirect("editor_dashboard")
                else:
                    msg = "Wrong email or password"
                    return render(request, 'loginpage.html', {'msg': msg})

            else:

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

                Users.objects.filter(id=someuser.id).update(password=newPassword)
                Users.objects.filter(id=someuser.id).update(attempt=0)
                
                msg = "Account is locked, please check email for new password"
                return render(request, 'loginpage.html', {'msg': msg})
        else:
            msg = "Wrong email or password"
            return render(request, 'loginpage.html', {'msg': msg})
    else:
        return render(request, "loginpage.html")


def cookie_session(request):
    try:
        email = request.POST['email']
        user_email = Users.objects.get(email=email)
        request.session['id'] = user_email.id
        request.session['role_id_id'] = user_email.role_id_id
    except:
        print("no session created")
