from django.shortcuts import render
from luna.models import *

def logoutpage(request):
    #Logout
    request.session.flush()
    return render(request, "home.html")