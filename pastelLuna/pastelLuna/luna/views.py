from django.http import HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib import messages


from .models import *
from .validator import *

def home(request):
    promotion = Promotion.objects.all()
    product = Product_Request.objects.filter(status="approve")
    return render(request, 'home.html', {'promotion': promotion, 'products': product} )


@csrf_exempt
def profile(request):
    # inner join with id where user id =1 (pass in through param)
    obj = Users.objects.select_related("role_id").filter(id=1)

    if request.method == 'POST':
        editProfile = Users.objects.get(id=1)
        if request.POST.get('save', '') == 'update':
            editProfile.first_name = request.POST.get('firstname')
            editProfile.last_name = request.POST.get('lastname')
            # input validation for phone textbox
            if not validate_phone_input(request, request.POST.get('mobile'), editProfile.phone):
                editProfile.phone = request.POST.get('mobile')
            # TODO input validation for address text box
            editProfile.address = request.POST.get("address")
            editProfile.allergies = request.POST.get("allergies")
            # Save to the database here
            editProfile.save()
            return HttpResponseRedirect(request.path_info)
    else:
        context = {"object": obj}
        return render(request, "profile.html", context)


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

@api_view(['GET', 'POST'])
def retrieve_product_details(request, slug): 
    product_Detail = get_object_or_404(Product_Details,slug=slug)
    product = {"product": product_Detail}
    if request.method == 'POST':
        user = Users.objects.get(id=1)
        if user is not None:
            if request.POST.get('add_to_cart', '') == 'product_add':
                product_id = int(request.POST.get('id'))
                product_price = request.POST.get('price')
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
                    else:
                        product_qty = 1
                        if product_status_qty >= product_qty:
                            # new_item = Cart.objects.create(user_id=user.id, product_id=product_id, quantity=product_qty, total_price=product_price)
                            Cart.objects.create(user_id=user, product_id=product_Detail, quantity=product_qty, total_price=product_price)
                            messages.success(request, 'Successfully added into cart')
                        else:
                            messages.error(request,'Failed to add into cart; Out of Stock!') 
        else:
            #replace with login page
            return render(request, "home.html")
        return redirect("product_details", slug=slug)
    elif request.method == 'GET':
        return render(request,"product_details.html", product)
    else:
        messages.error(request,'Failed to add into cart; Try Again Later')
        return render(request,"product_details.html", product)


def shop(request):
    #product = Product_Details.objects.all()
    product = Product_Request.objects.filter(status="approve")
    return render(request, 'shop.html', {'products': product})