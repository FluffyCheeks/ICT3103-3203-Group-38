from django.shortcuts import render, get_object_or_404

from luna.models import *
from luna.validator import *


def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var


def home(request):
    check_for_cookie_session(request)
    if not check_for_cookie_session(request) or check_for_cookie_session(request) == 1:
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
    else:
        return render(request, "unauthorised_user.html")


def shop(request):
    check_for_cookie_session(request)

    if not check_for_cookie_session(request) or check_for_cookie_session(request) == 1:
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
    check_for_cookie_session(request)

    if not check_for_cookie_session(request) or check_for_cookie_session(request) == 1:
        num_of_prod = Cart.objects.filter(user_id=1)
        return render(request, 'base.html', {'products_num': num_of_prod})
    else:
        num_of_prod = 0
        return render(request, 'base.html', {'products_num': num_of_prod})
