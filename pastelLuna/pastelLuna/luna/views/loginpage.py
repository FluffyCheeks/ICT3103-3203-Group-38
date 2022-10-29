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
        exist_password = Users.objects.filter(password=password).exists()

        if exist_username:
            someuser = Users.objects.get(email__contains=email)
            if someuser.password == password:
                if someuser is not None:
                    session_id = cookie_session(request)
                    return render(request, "profile.html", {"session_id" : session_id})
            else:
                msg = "Wrong email or password"
                return render(request, 'loginpage.html', {'msg': msg})
        else:
            msg = "Wrong email or password"
            return render(request, 'loginpage.html', {'msg': msg})
    else:
        return render(request, "loginpage.html")


def cookie_session(request):
    # request.session.set_test_cookie()
    #print("Request", type(request.session))

    email = request.POST['email']
    user_email = Users.objects.get(email=email)

    #print("User email is ", user_email.id)
    request.session['id'] = user_email.id
    return request.session['id']

def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    else:
        print("No session")