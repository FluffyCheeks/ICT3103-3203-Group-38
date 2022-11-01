from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from luna.serializers import ProductSerializer
# from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
# from rest_framework import status
from luna.models import *
import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from luna.models import *
from luna.validator import *

@csrf_exempt
#@login_required(login_url='login')
def viewcart(request):
    # static filer for cart need to change once addtocart is implemented
    cart = Cart.objects.select_related("user_id").filter(user_id=1)
    total_price = 0
    quantity = 0
    for item in cart:
        total_price = total_price + item.quantity * item.total_price
        quantity = quantity + item.quantity 
    context = {"cart": cart, 'total_price':total_price, 'quantity':quantity}
    return render(request, "cart.html", context)

    #dynamic filter base on user
        #cart = Cart.objects.filter(user=request.user)
        #context = {"cart": cart}
        #return render(request, "cart.html", context)

@csrf_exempt
def updatecart(request):
    userid = Users.objects.get(id=1)
    prodID = int(request.POST.get('product_id'))
    if request.method == 'POST':
        if(Cart.objects.filter( user_id  = userid, product_id = prodID )):
            prod_qty = (request.POST.get('quanity'))
            cart = Cart.objects.get( product_id = prodID, user_id  = userid,)
            cart.quantity = prod_qty
            cart.save()
            messages.success(request, 'Updated successfully')
        return JsonResponse({'status': "Updated Successfully"})
    return redirect('/')

#def updatecart(request):
    #if request.method == 'POST':
        #string = request.POST.get('product_id')
        #prodID = int(re.sub('[^0-9]', '', string)) #get the int  
        #if(Cart.objects.filter(user=request.user, product_id = prodID )):
           # prod_qty = (request.POST.get('quanity'))
           # cart = Cart.objects.get(product_id = prodID, user=request.user,)
            #cart.quantity = prod_qty
            #cart.save()
        #return JsonResponse({'status': "Updated Successfully"})
   # return redirect('/')

@csrf_exempt
def deletecartitem(request):
    if request.method == 'POST':
        userid = Users.objects.get(id=1)
        prodID = request.POST.get('product_id')
        if(Cart.objects.filter( user_id  = userid, product_id = prodID )):
            cart = Cart.objects.get(product_id = prodID , user_id  = userid)
            cart.delete()
            messages.success(request, 'Deleletd successfully')
        return JsonResponse({'status': "Deleted Successfully"})
    return redirect('/')