from django.shortcuts import redirect, render
import re
from luna.models import *
from luna.validator import *

from django.utils.translation import gettext_lazy as _

def orderdetail (request):
    uid = request.session['id']
    profileorder = Users.objects.select_related("role_id").filter(id=uid)

    #orderinfo = Orders.objects.filter(user=request.user)
    orderinfo = Orders.objects.select_related("user").filter(user_id=uid)

    context = {'profileorder':profileorder , 'orderinfo':orderinfo}
    return render(request, "orderdetail.html", context)