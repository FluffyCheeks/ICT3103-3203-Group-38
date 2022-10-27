from django.shortcuts import render


from luna.models import *
from luna.validator import *

def home(request):
    # showcart(request)
    num_of_prod = Cart.objects.filter(user_id=1)
    promotion = Promotion.objects.all()
    product = Product_Request.objects.filter(status="approve")
    return render(request, 'home.html', {'promotion': promotion, 'products': product, 'products_num': num_of_prod} )

def shop(request):
    product = Product_Request.objects.filter(status="approve")
    return render(request, 'shop.html', {'products': product})

    # def showcart_base(request):
    # num_of_prod = Cart.objects.filter(user_id=1)
    # return render(request, 'base.html', {'products_num': num_of_prod})