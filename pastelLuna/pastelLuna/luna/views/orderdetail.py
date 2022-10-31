import random as rand
from django.shortcuts import redirect, render
from django.contrib.sessions import base_session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import re
from luna.models import *
from luna.validator import *

from django.utils.translation import gettext_lazy as _

def orderdetail (request):
     # profileorder = Users.objects.filter(user=request.user)
    uid = request.session['id']
    profileorder = Users.objects.select_related("role_id").filter(id=uid)

    #orderinfo = Orders.objects.filter(user=request.user)
    orderinfo = Orders.objects.select_related("user").filter(user_id=uid)


    context = {'profileorder':profileorder , 'orderinfo':orderinfo}
    return render(request, "orderdetail.html", context)