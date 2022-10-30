from django.shortcuts import render
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

        dBPassword = str(dBPassword).replace("b'","").replace("'","") 
        dBPassword = dBPassword.encode('utf-8')

        if exist_username:
            someuser = Users.objects.get(email__contains=email)
            if bcrypt.checkpw(password, dBPassword):
                if someuser is not None:
                    cookie_session(request)
                    return render(request, "profile.html")
            else:
                msg = "Wrong email or password"
                return render(request, 'loginpage.html', {'msg': msg})
        else:
            msg = "Wrong email or password"
            return render(request, 'loginpage.html', {'msg': msg})
    else:
        return render(request, "loginpage.html")

def cookie_session(request):
    email = request.POST['email']
    user_email = Users.objects.get(email=email)
    request.session['id'] = user_email.id
