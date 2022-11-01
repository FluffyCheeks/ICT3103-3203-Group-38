from django.shortcuts import render, get_object_or_404

from luna.models import *
from luna.validator import *


def home(request):

    promotion = Promotion.objects.all()
    product = Product_Request.objects.filter(status="approve")
    if request.method == 'POST':
        if request.POST.get('searchName', '') == 'search':
            res = request.POST.get('searchInput')
            print(res)
            product_Detail = get_object_or_404(Product_Details, slug=res)
            product = {"product": product_Detail}
            return render(request, 'product_details.html', product)

    return render(request, 'home.html', {'promotion': promotion, 'products': product})


def shop(request):
    if request.session['role_id_id'] == 1:
        product = Product_Request.objects.filter(status="approve")
        if request.method == 'POST':
            if request.POST.get('searchName', '') == 'search':
                res = request.POST.get('searchInput')
                print(res)
                product_Detail = get_object_or_404(Product_Details, slug=res)
                product = {"product": product_Detail}
                return render(request, 'product_details.html', product)

        return render(request, 'shop.html', {'products': product})
    else:
        return render(request, "unauthorised_user.html")


def showcart_base(request):
    # needs to add into session
    if request.session['role_id_id'] == 1:
        num_of_prod = Cart.objects.filter(user_id=1)
        return render(request, 'base.html', {'products_num': num_of_prod})
    else:
        num_of_prod = 0
        return render(request, 'base.html', {'products_num': num_of_prod})
