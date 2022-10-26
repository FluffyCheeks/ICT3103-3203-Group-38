import random as rand
from django.shortcuts import redirect, render
from django.contrib.sessions import base_session

from django.contrib.auth.decorators import login_required
from .models import *
import re
from .validator import *

from django.utils.translation import gettext_lazy as _

def orderdetail (request):
     # profileorder = Users.objects.filter(user=request.user)
    profileorder = Users.objects.select_related("role_id").filter(id=1)

    #orderinfo = Orders.objects.filter(user=request.user)
    orderinfo = Orders.objects.select_related("user").filter(user_id=1)


    context = {'profileorder':profileorder , 'orderinfo':orderinfo}
    return render(request, "orderdetail.html", context)