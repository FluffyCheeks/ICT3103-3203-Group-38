from tokenize import Double
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile
from django.core import serializers
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

from luna.models import *
from luna.validator import *


@api_view(['GET', 'POST'])
def editor_dashboard(request,id=None):
    # uid = request.session['id']
    
    user = Authorised_User.objects.get(id=1) 
    cat = Product_Category.objects.all()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        prod_details = request.POST.get('edit_id')
        if Product_Details.objects.filter(id=prod_details):
            try:
                cat_id =  Product_Details.objects.values_list('category_id', flat=True).get(id=prod_details)
                prod_details = Product_Details.objects.get(id=prod_details)
                prod_data = serializers.serialize("json", [prod_details])
            except:
                print("Error has occurred, Please try again later.")
            prod_cat = Product_Category.objects.get(id=cat_id)
            cat_data = serializers.serialize("json", [prod_cat])
            print("PRODUCT JSON --- ", prod_data)
            return JsonResponse({ 'product' : prod_data, 'cat': cat_data})
    elif request.method == 'POST':
        if request.POST.get('product_req_add', '') == 'add_request':
            image_form = request.FILES['image_upload']
            image_name = request.POST.get('imagename') 
            product_name = request.POST.get('productname')
            product_desc = request.POST.get('productdesc')
            prod_ingredients = request.POST.get('ingredientsText')
            unit_price = request.POST.get('unitprice')
            stocks = request.POST.get('stocks')
            category = request.POST.get('category')
            date_created = datetime.now()
            formatedDate = date_created.strftime("%Y-%m-%d %H:%M:%S")

            temp_imgn = image_name + ".jpg"
            while validate_product(request, image_form, image_name, product_name, product_desc, unit_price, stocks, category, prod_ingredients):
                if request.FILES['image_upload'].name == temp_imgn:
                    if category == 'others':
                        Product_Category.objects.get_or_create(category_name=request.POST.get('category_input'))
                        cat = Product_Category.objects.filter(category_name=request.POST.get('category_input'))
                    else:
                        cat = Product_Category.objects.get(id=request.POST.get('category'))
                    prod_request = Product_Details.objects.create(category_id =cat, slug=image_name, name=product_name, description=product_desc, ingredients=prod_ingredients, unit_price=float(unit_price),
                                                                    stock_available=int(stocks),image=request.FILES['image_upload'].name )
                    fs = FileSystemStorage()
                    fs.save(image_form.name, image_form)
                    print("in editor dashboard __ POST-- CREATED DETAIL")
                    Product_Request.objects.create(product_id=prod_request,user_id=user,status="pending", created=formatedDate)
                    messages.success(request, 'Successfully added request -- Pending')
                else:
                    messages.error(request, 'Product Image name must be same as Image file name')
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info)
        elif request.POST.get('edit_to_cart', '') == 'product_edit':
            image_form = request.FILES['image_upload']
            image_name = request.POST.get('imagename') 
            product_name = request.POST.get('productname')
            product_desc = request.POST.get('productdesc')
            prod_ingredients = request.POST.get('ingredientsText')
            unit_price = request.POST.get('unitprice')
            stocks = request.POST.get('stocks')
            category = request.POST.get('category')
            date_updated = datetime.now()
            formatedDate = date_updated.strftime("%Y-%m-%d %H:%M:%S")
            temp_imgn = image_name + ".jpg"
            while validate_product(request, image_form, image_name, product_name, product_desc, unit_price, stocks, category, prod_ingredients):
                if category == 'others':
                    Product_Category.objects.get_or_create(category_name=request.POST.get('category_input'))
                    cat = Product_Category.objects.filter(category_name=request.POST.get('category_input'))
                else:
                    cat = Product_Category.objects.get(id=request.POST.get('category'))
                prod_request = Product_Details.objects.save(category_id =cat, slug=image_name, name=product_name, description=product_desc, ingredients=prod_ingredients, unit_price=float(unit_price),
                                                                stock_available=int(stocks),image=request.FILES['image_upload'].name )
                fs = FileSystemStorage()
                fs.save(image_form.name, image_form)
                Product_Request.objects.create(product_id=prod_request,user_id=user,status="pending", created=formatedDate)
                messages.success(request, 'Successfully edited request -- Pending')
                return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(request.path_info)
    else: 
        print("in editor dashboard -- GET")
        product_req = Product_Request.objects.filter(user_id=1).order_by('created')
        return render(request, 'editor_dashboard.html', {'products': product_req, 'cat': cat})

