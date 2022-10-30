from django.shortcuts import redirect
from luna.models import *


def logoutpage(request):
    # Logout
    request.session.flush()
    response = redirect('/')
    return response
