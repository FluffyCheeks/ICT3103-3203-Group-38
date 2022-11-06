from django.shortcuts import render
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.html import escape

from luna.models import *


def aboutus(request):
    num_cart = showcart_base(request) 
    return render(request, "aboutus.html",{'products_num': num_cart})


def showcart_base(request):
    # needs to add into session
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 1:
        uid = escape(request.session['id'])
        num_of_prod = Cart.objects.filter(user_id=uid)
        print(num_of_prod.count, "---- COUNTR")
        return num_of_prod.count
    else:
        num_of_prod = 0
        return num_of_prod

def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var