from django.http import HttpResponseRedirect
from django.shortcuts import render

from luna.models import *
from luna.validator import *



def editor_dash(request):
    product = Product_Request.objects.filter(status="approve")
    return render(request, 'shop.html', {'products': product}) 