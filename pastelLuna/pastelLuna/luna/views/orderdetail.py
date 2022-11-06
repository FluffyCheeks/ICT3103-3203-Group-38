from django.shortcuts import redirect, render
import re
from luna.models import *
from luna.validator import *

from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.html import escape

from django.utils.translation import gettext_lazy as _

def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var

def orderdetail (request):
    check_for_cookie_session(request)
    num_cart = showcart_base(request) 
    if check_for_cookie_session(request) == 1:
        uid = request.session['id']
        profileorder = Users.objects.select_related("role_id").filter(id=uid)

        #orderinfo = Orders.objects.filter(user=request.user)
        orderinfo = Orders.objects.select_related("user").filter(user_id=uid)


        context = {'profileorder':profileorder , 'orderinfo':orderinfo,  'products_num': num_cart}
        return render(request, "orderdetail.html", context)
    else:
        return render(request, "unauthorised_user.html")


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