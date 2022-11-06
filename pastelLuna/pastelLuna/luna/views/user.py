from tokenize import Double
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile
from django.core import serializers
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.clickjacking import xframe_options_deny
from django.utils.html import escape

from luna.models import *
from luna.validator import *

@sensitive_variables('id')
@sensitive_post_parameters
@api_view(['GET', 'POST'])
def editor_dashboard(request,id=None):
    check_for_cookie_session(request)
    if check_for_cookie_session(request) == 3:
        uid = escape(request.session['id'])
        fromtableuser = Users.objects.get(id=uid)
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
                return JsonResponse({ 'product' : prod_data, 'cat': cat_data})
        elif request.method == 'POST':
            if request.POST.get('product_req_add', '') == 'add_request':
                print('add')
                image_form = request.FILES['image_upload']
                product_name = escape(request.POST.get('productname'))
                product_desc = escape(request.POST.get('productdesc'))
                prod_ingredients = escape(request.POST.get('ingredientsText'))
                unit_price = escape(request.POST.get('unitprice'))
                stocks = escape(request.POST.get('stocks'))
                category = escape(request.POST.get('category'))
                date_created = datetime.now()
                formatedDate = date_created.strftime("%Y-%m-%d %H:%M:%S")
                print("oimage form --", image_form)
                temp_imgn = request.FILES['image_upload'].name
                while validate_product_new(request, image_form, product_name, product_desc, unit_price, stocks, category, prod_ingredients):
                    if request.FILES['image_upload'].name == temp_imgn:
                        if category == 'others':
                            Product_Category.objects.get_or_create(category_name=request.POST.get('category_input'))
                            cat = Product_Category.objects.filter(category_name=request.POST.get('category_input'))
                        else:
                            cat = Product_Category.objects.get(id=request.POST.get('category'))
                        prod_request = Product_Details.objects.create(category_id =cat, slug=temp_imgn, name=product_name, description=product_desc, ingredients=prod_ingredients, unit_price=float(unit_price),
                                                                        stock_available=int(stocks),image=request.FILES['image_upload'].name )
                        fs = FileSystemStorage()
                        fs.save(image_form.name, image_form)
                        print("in editor dashboard __ POST-- CREATED DETAIL")
                        Product_Request.objects.create(user_pk_id_id=fromtableuser, user_id=user,product_id=prod_request, status="pending", created=formatedDate)
                        messages.success(request, 'Successfully added request -- Pending')
                    else:
                        messages.error(request, 'Product Image name must be same as Image file name')
                    return HttpResponseRedirect(request.path_info)
                return HttpResponseRedirect(request.path_info)
            elif request.POST.get('edit_to_cart', '') == 'product_edit':
                print("in editor dashboard __ EDIT")
                prod_details = escape(request.POST.get('edit_id'))
                image_name = escape(request.POST.get('imagename')) 
                product_name = escape(request.POST.get('productname'))
                product_desc = escape(request.POST.get('productdesc'))
                prod_ingredients = escape(request.POST.get('ingredientsText'))
                unit_price = escape(request.POST.get('unitprice'))
                stocks = escape(request.POST.get('stocks'))
                category = escape(request.POST.get('category'))
                date_updated = datetime.now()
                formatedDate = date_updated.strftime("%Y-%m-%d %H:%M:%S")
                temp_imgn = image_name + ".jpg"
                while validate_product(request, image_name, product_name, product_desc, unit_price, stocks, category, prod_ingredients):
                    if category == 'others':
                        Product_Category.objects.get_or_create(category_name=request.POST.get('category_input'))
                        cat = Product_Category.objects.filter(category_name=request.POST.get('category_input'))
                    else:
                        cat = Product_Category.objects.get(id=request.POST.get('category'))
                    if 'image_upload' not in request.FILES:
                        Product_Details.objects.filter(id=prod_details).update(category_id =cat, name=product_name, description=product_desc, ingredients=prod_ingredients, unit_price=float(unit_price),
                                                                    stock_available=int(stocks))
                    else: 
                        image_form = request.FILES['image_upload']
                        validated = validate_image(request, image_form)
                        if validated:
                            Product_Details.objects.filter(id=prod_details).update(category_id =cat, slug=temp_imgn, name=product_name, description=product_desc, ingredients=prod_ingredients, unit_price=float(unit_price),
                                                                    stock_available=int(stocks),image=image_form.name)
                        fs = FileSystemStorage()
                        fs.save(image_form.name, image_form)
                    prod_request = Product_Details.objects.get(id=prod_details)
                    Product_Request.objects.filter(product_id=prod_request, status="pending").update(user_id=user, updated=formatedDate)
                    messages.success(request, 'Successfully edited request -- Pending')
                    return HttpResponseRedirect(request.path_info)
                return HttpResponseRedirect(request.path_info)
        else: 
            print("in editor dashboard -- GET")
            product_req = Product_Request.objects.filter(user_id=1).order_by('-created')
            return render(request, 'editor_dashboard.html', {'products': product_req, 'cat': cat})
        return render(request, 'editor_dashboard.html', {'products': product_req})
    else:
        return render(request, 'unauthorised_user.html')

@sensitive_variables('role_id_id')
def check_for_cookie_session(request):
    try:
        id = request.session['role_id_id']
        return id
    except:
        var = False
        return var