from django.shortcuts import render,  get_object_or_404, redirect
from rest_framework.decorators import api_view
from django.contrib import messages
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.html import escape

from luna.models import *
from luna.validator import *


@sensitive_variables()
def check_for_cookie_session(request):
    try:
        id = escape(request.session['role_id_id'])
        print("role-IDID-----", id)
        return id
    except:
        var = False
        return var

@sensitive_post_parameters()
@api_view(['GET', 'POST'])
def retrieve_product_details(request, slug):
    if check_for_cookie_session(request) != 2 or check_for_cookie_session(request) != 3:
        product_Detail = get_object_or_404(Product_Details,slug=slug)
        print(product_Detail.id, "FROM DB")
        num_cart = showcart_base(request) 
        print(request.session['id'])
        context = {"product": product_Detail,  'products_num': num_cart}
        if request.method == 'POST':
            if check_for_cookie_session(request):
                uid = escape(request.session['id'])
                user = Users.objects.get(id=uid)
                if user is not None:
                    if request.POST.get('add_to_cart', '') == 'product_add':
                        product_id = escape(int(request.POST.get('id')))
                        print(product_id, "-- FROM TEMP")
                        product_price = escape(request.POST.get('price'))
                        if product_Detail.id == product_id:
                            product_status_qty = product_Detail.stock_available
                            item_in_cart = Cart.objects.filter(user_id=user.id, product_id=product_id)
                            if item_in_cart:
                                item = Cart.objects.get(user_id=user.id, product_id=product_id)
                                product_qty = item.quantity
                                product_qty +=1
                                item.quantity = product_qty
                                item.save()
                                messages.success(request, 'Successfully added into cart --- Quantity has been updated')
                                return redirect("shop")
                            else:
                                product_qty = 1
                                if product_status_qty >= product_qty:
                                    Cart.objects.create(user_id=user, product_id=product_Detail, quantity=product_qty, total_price=product_price)
                                    messages.success(request, 'Successfully added into cart')
                                    return redirect("shop")
                                else:
                                    messages.error(request,'Failed to add into cart; Out of Stock!')
                                    return redirect("shop")
                        else:
                            messages.error(request, 'Error occurred, Please Try Again Later.')
                            return redirect("/")
                else:
                    return redirect("loginpage")
            else:
                return redirect("loginpage")
            # return redirect("/", slug=slug)
        elif request.method == 'GET':
            return render(request,"product_details.html", context)
        else:
            messages.error(request,'Failed to add into cart; Try Again Later')
            return redirect("/luna/product_details")
    else:
        return render(request, "unauthorised_user.html")


@sensitive_variables('id')
def showcart_base(request):
    # needs to add into session
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 1:
        uid = escape(request.session['id'])
        print("")
        num_of_prod = Cart.objects.filter(user_id=uid)
        print(num_of_prod.count, "---- COUNTR")
        return num_of_prod.count
    else:
        num_of_prod = 0
        uid = escape(request.session['id'])
        print("uid ----", uid)
        print(num_of_prod, "---- IN 0")
        return num_of_prod