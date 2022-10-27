from django.shortcuts import render,  get_object_or_404, redirect
from rest_framework.decorators import api_view
from django.contrib import messages

from luna.models import *
from luna.validator import *

@api_view(['GET', 'POST'])
def retrieve_product_details(request, slug): 
    product_Detail = get_object_or_404(Product_Details,slug=slug)
    product = {"product": product_Detail}
    if request.method == 'POST':
        user = Users.objects.get(id=1) #edit by login user session
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
        return redirect("/", slug=slug)
    elif request.method == 'GET':
        return render(request,"product_details.html", product)
    else:
        messages.error(request,'Failed to add into cart; Try Again Later')
        return render(request,"product_details.html", product)

