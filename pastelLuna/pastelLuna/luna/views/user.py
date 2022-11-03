from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view

from luna.models import *
from luna.validator import *


def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var


@api_view(['GET', 'POST'])
def editor_dashboard(request):
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 3:
        product_req = Product_Request.objects.filter(user_id=1)
        return render(request, 'editor_dashboard.html', {'products': product_req})
    else:
        return render(request, 'unauthorised_user.html')
