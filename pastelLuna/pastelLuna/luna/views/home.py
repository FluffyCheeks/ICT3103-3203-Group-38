from django.shortcuts import render, get_object_or_404
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.html import escape

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
        num_cart = showcart_base(request) 
        if request.method == 'POST':
            if request.POST.get('searchName', '') == 'search':
                res = escape(request.POST.get('searchInput'))
                print(res)
                product_Detail = get_object_or_404(Product_Details, slug=res)
                product = {"product": product_Detail}
                return render(request, 'product_details.html',{'product': product_Detail, 'products_num': num_cart})

        return render(request, 'home.html', {'promotion': promotion, 'products': product, 'products_num': num_cart})
    else:
        return render(request, "unauthorised_user.html")


def shop(request):
    check_for_cookie_session(request)
    if not check_for_cookie_session(request) or check_for_cookie_session(request) == 1:
        product = Product_Request.objects.filter(status="approve")
        num_cart = showcart_base(request) 
        if request.method == 'POST':
            if request.POST.get('searchName', '') == 'search':
                res = escape(request.POST.get('searchInput'))
                print(res)
                product_Detail = get_object_or_404(Product_Details, slug=res)
                product = {"product": product_Detail}
                return render(request, 'product_details.html', product)
            return render(request, 'shop.html', {'products': product, 'products_num': num_cart})
        return render(request, 'shop.html', {'products': product, 'products_num': num_cart})
    else:
        return render(request, "unauthorised_user.html")


def showcart_base(request):
    # needs to add into session
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 1:
        uid = escape(request.session['id'])
        num_of_prod = Cart.objects.filter(user_id=uid)
        print(num_of_prod.count, "---- COUNTR")
        return num_of_prod.count
    else:
        num_of_prod = 0
        return num_of_prod
