from django.shortcuts import redirect, render
import re
from luna.models import *
from luna.validator import *

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
    if check_for_cookie_session(request) == 1:
        uid = request.session['id']
        profileorder = Users.objects.select_related("role_id").filter(id=uid)

        #orderinfo = Orders.objects.filter(user=request.user)
        orderinfo = Orders.objects.select_related("user").filter(user_id=uid)


        context = {'profileorder':profileorder , 'orderinfo':orderinfo}
        return render(request, "orderdetail.html", context)
    else:
        return render(request, "unauthorised_user.html")