from django.shortcuts import render, redirect
from luna.models import *
import bcrypt


def loginpage(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
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
            if bcrypt.checkpw(password, dBPassword):
                if someuser is not None:
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
