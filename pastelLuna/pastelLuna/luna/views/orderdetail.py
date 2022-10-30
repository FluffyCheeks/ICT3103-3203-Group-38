import random as rand
from django.shortcuts import redirect, render
from django.contrib.sessions import base_session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import re
from luna.models import *
from luna.validator import *

from django.utils.translation import gettext_lazy as _
@csrf_exempt
def orderdetail (request):
     # profileorder = Users.objects.filter(user=request.user)
    profileorder = Users.objects.select_related("role_id").filter(id=1)

    #orderinfo = Orders.objects.filter(user=request.user)
    orderinfo = Orders.objects.select_related("user").filter(user_id=1)


    context = {'profileorder':profileorder , 'orderinfo':orderinfo}
    return render(request, "orderdetail.html", context)