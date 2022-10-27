
import decimal
import random as rand
from unicodedata import name
from django.shortcuts import redirect, render
from django.contrib.sessions import base_session

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from luna.models import *
from luna.validator import *
import re

from django.utils.translation import gettext_lazy as _

@csrf_exempt
#@login_required(login_url='login')
def checkout (request):
    #for now static specific a id
    profileorder = Users.objects.select_related("role_id").filter(id=1)
    rawcart = Cart.objects.select_related("user_id").filter(user_id=1)
    #rawcart = Cart.objects.filter(user=request.user)
   
    for item in rawcart:
        if item.quantity > item.product_id.stock_available:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.select_related("user_id").filter(user_id=1)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.total_price * item.quantity
    
    context = {'cartitems':cartitems, 'total_price':total_price, 'rawcart':rawcart, 'profileorder':profileorder}
    return render(request, "checkout.html", context)




def validate_credit_card(cardnumber):
    if len(cardnumber) == 16:
            for i in range(0, len(cardnumber)):
                cardnumber[i] = int(cardnumber[i])
            last = cardnumber[15]
            first = cardnumber[:15]
            first = first[::-1]
            
            for i in range(len(first)):
                if i % 2 == 0:
                    first[i] = first[i] * 2
                if first[i] > 9:
                    first[i] -= 9
            sum_all = sum(first)
        
            t1 = sum_all % 10
            t2 = t1 + last
            if t2 % 10 == 0:
                return True
            else:
                return False         
    else:
        print("Credit Card number limit Exceeded!!!!")
        exit()

def mask_cc_number(cc_string, digits_to_keep=4, mask_char='*'):
   cc_string_total = sum(map(str.isdigit, cc_string))

   if digits_to_keep >= cc_string_total:
       print("Not enough numbers. Add 10 or more numbers to the credit card number.")

   digits_to_mask = cc_string_total - digits_to_keep
   masked_cc_string = re.sub('\d', mask_char, cc_string, digits_to_mask)

   return masked_cc_string

#Validation #UserDATAFIELD
def clean_inputfield(self):
    special_char=re.compile('[@_!$%^&*()<>?/\|}{~:]')
    if special_char.search(self) == None:
            return True
    return False

def clean_Phoneno(self):
    special_char=re.compile('[@_!$%^&*()<>?/\|}{~:]#')
    if special_char.search(self) == None:
        if (self.isdigit() and len(self) == 8):
            return True
    return False

def clean_emailaddress(self):
    special_char=re.compile('[!$%^&*()<>?/\|}{~:]')
    if special_char.search(self) == None:
            return True
    return False

#@login_required(login_url='login')
@csrf_exempt
def placeorder (request):
    if request.method == 'POST' and 'payment_mode1' in request.POST:
        cardnumber = request.POST.get('creditCradNum')
        fistn = request.POST.get('fname')
        lastn = request.POST.get('lname')
        disccode = request.POST.get('disc')
        phonenumber = request.POST.get('Phoneno')
        address = request.POST.get('Addr')
        email = request.POST.get('email')
        sanitizeph = phonenumber
        list1 = list(cardnumber)
        if (validate_credit_card(list1) and clean_Phoneno(sanitizeph) and clean_emailaddress(email) and clean_emailaddress(address) and clean_inputfield(fistn) and clean_inputfield(lastn) and clean_inputfield(disccode)) == 1:
            neworder = Orders()
            #neworder.user = request.user
            neworder.first_name = request.POST.get('fname')
            neworder.last_name = request.POST.get('lname')
            neworder.email = request.POST.get('email')
            neworder.phone = request.POST.get('Phoneno')
            neworder.user = Users.objects.get(id=1) #currently static need to change
            neworder.address = request.POST.get('Addr')
            neworder.payment_mode = request.POST.get('payment_mode1')
            Masked = mask_cc_number(request.POST.get('creditCradNum'))
            neworder.ccard_digits = Masked
            discode =  request.POST.get('disc')

            #cart = Cart.objects.filter(user=request.user)
            cart = Cart.objects.select_related("user_id").filter(user_id=1)
            cart_total_price = 0
            for item in cart:
                cart_total_price = cart_total_price + item.total_price * item.quantity
        
            discountcode = "10OFF"
            if discode == discountcode:
                neworder.total_price = cart_total_price - decimal.Decimal(float('10.00'))
            else:
                neworder.total_price = cart_total_price

            trackno = 'sharma'+ str(rand.randint(1000000000, 9999999999))
            while Orders.objects.filter(tracking_no = trackno) is None:
                trackno = 'sharma'+str(rand.randint(1000000000, 9999999999))

            neworder.tracking_no = trackno
            neworder.save()
            
            
            #neworderItem = Cart.objects.filter(user=request.user)
            neworderItem = Cart.objects.select_related("user_id").filter(user_id=1)
            for item in neworderItem:
                OrderItem.objects.create(
                order = neworder,
                productID = item.product_id,
                price = item.quantity * item.total_price,
                quantity = item.quantity
                )
                #decrease product qty from names
                string =str(item.product_id)     
                prodID = string
                orderproduct = Product_Details.objects.filter(name=prodID).first()
                orderproduct.stock_available = orderproduct.stock_available - item.quantity
                orderproduct.save()

                
            # Cart.objects.filter(user=request.user).delete()
            Cart.objects.select_related("user_id").filter(user_id=1).delete()
            messages.success(request, 'Order Success, Thank you for the order')
            return redirect('/luna/checkout')
        else:
            messages.success(request, 'Order Not success, Please enter a Valid credit card number and valid required field')
            return redirect('/luna/checkout')

    if request.method == 'POST' and 'payment_mode' in request.POST:
        fistn = request.POST.get('fname')
        lastn = request.POST.get('lname')
        disccode = request.POST.get('disc')
        phonenumber = request.POST.get('Phoneno')
        address = request.POST.get('Addr')
        email = request.POST.get('email')
        sanitizeph = phonenumber
        if (clean_Phoneno(sanitizeph) and clean_emailaddress(email) and clean_emailaddress(address) and clean_inputfield(fistn) and clean_inputfield(lastn) and clean_inputfield(disccode)) == 1:
            neworder = Orders()
            #neworder.user = request.user
            neworder.first_name = request.POST.get('fname')
            neworder.last_name = request.POST.get('lname')
            neworder.email = request.POST.get('email')
            neworder.phone = request.POST.get('Phoneno')
            neworder.user = Users.objects.get(id=1) #currently static need to change
            neworder.address = request.POST.get('Addr')
            neworder.payment_mode = request.POST.get('payment_mode')
            discode =  request.POST.get('disc')
            
            #cart = Cart.objects.filter(user=request.user)
            cart = Cart.objects.select_related("user_id").filter(user_id=1)
            cart_total_price = 0
            for item in cart:
                cart_total_price = cart_total_price + item.total_price * item.quantity
        
            discountcode = "10OFF"
            if discode == discountcode:
                neworder.total_price = cart_total_price - decimal.Decimal(float('10.00'))
                if neworder.total_price < 0:
                    neworder.total_price = 0
            else:
                neworder.total_price = cart_total_price

            trackno = 'sharma'+ str(rand.randint(1000000000, 9999999999))
            while Orders.objects.filter(tracking_no = trackno) is None:
                trackno = 'sharma'+str(rand.randint(1000000000, 9999999999))

            neworder.tracking_no = trackno
            neworder.save()
            
            
            #neworderItem = Cart.objects.filter(user=request.user)
            neworderItem = Cart.objects.select_related("user_id").filter(user_id=1)
            for item in neworderItem:
                OrderItem.objects.create(
                order = neworder,
                productID = item.product_id,
                price = item.quantity * item.total_price,
                quantity = item.quantity
                )
                #decrease product qty from stock base on name
                string =str(item.product_id)     
                prodID = string
                orderproduct = Product_Details.objects.filter(name=prodID).first()
                orderproduct.stock_available = orderproduct.stock_available - item.quantity
                orderproduct.save()

                
            # Cart.objects.filter(user=request.user).delete()
            Cart.objects.select_related("user_id").filter(user_id=1).delete()
            messages.success(request, 'Order Success, Thank you for the order')
            return redirect('/luna/checkout')

        else:
            messages.success(request, 'Order Not success, Please enter valid user required field')
            return redirect('/luna/checkout')
    else:
        messages.success(request, 'Order Not Success, Please re-order again')
        return redirect('/luna/checkout')



