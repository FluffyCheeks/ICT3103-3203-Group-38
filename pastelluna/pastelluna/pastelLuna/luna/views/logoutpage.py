from django.shortcuts import render
from luna.models import *

def logoutpage(request):
    request.session.flush()
    if request.session.test_cookie_worked():
        cookie_delete(request)# Double check the code
        return render(request, "profile.html")
    return render(request, "home.html")