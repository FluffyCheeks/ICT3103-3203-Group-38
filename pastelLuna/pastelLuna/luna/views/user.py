from tokenize import Imagnumber
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view

from luna.models import *
from luna.validator import *
from luna.forms import PDForm




@api_view(['GET', 'POST'])
def editor_dashboard(request):
    print("in editor dashboard")
    user = Users.objects.get(id=1) 
    if request.method == 'POST':     
        print("in editor dashboard __ POST")
        if request.POST.get('product_req_add', '') == 'add_request':
            form = PDForm(request.POST, request.FILES)
            image_name = request.POST.get('imagename') 
            product_name = request.POST.get('productname')
            product_desc = request.POST.get('descriptionText')
            prod_ingredients = request.POST.get('ingredientsText')
            unit_price = request.POST.get('unitprice')
            stocks = request.POST.get('stocks')
            category = request.POST.get('category')
            if form.is_valid:
                form.save()
                while registration_validation(request, image_name, product_name, product_desc, unit_price, stocks, category, prod_ingredients):
                    if category == 'others':
                        Product_Category.objects.create(category_name=request.POST.get('category_input'))
                    cat = Product_Category.objects.filter(category_name=request.POST.get('category_input'))
                    prod_request = Product_Details.objects.create(category_id =cat.id, slug=image_name, name=product_name, description=product_desc, ingredients=prod_ingredients, unit_price=unit_price,
                                                                    stock_available=stocks)
                    Product_Request.objects.create(product_id= prod_request.id,user_id=user.id,status="pending")
                    messages.success(request, 'Successfully added request -- Pending')
                    return HttpResponseRedirect(request.path_info)
        # elif request.POST.get('add_request', '') == 'add_request':
    else: 
        print("in editor dashboard -- GET")
        product_req = Product_Request.objects.filter(user_id=1)
        return render(request, 'editor_dashboard.html', {'products': product_req})



