from django.http import HttpResponseRedirect
from django.shortcuts import render

from luna.models import *
from luna.validator import *


def registration(request):
    if request.method == 'POST':
        if request.POST.get('signup', '') == 'signup_confirm':
            urunler = Users.objects.create(role_id_id = 1, 
            first_name = request.POST.get('first_name'), 
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            allergies = request.POST.get('allergies'),
            password = request.POST.get('password'))
            urunler.save()
            return HttpResponseRedirect(request.path_info)
    return render(request, 'registration.html')

def editor_dash(request):
    product = Product_Request.objects.filter(status="approve")
    return render(request, 'shop.html', {'products': product}) 