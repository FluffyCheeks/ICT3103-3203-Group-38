from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view


from luna.models import *
from luna.validator import *



@api_view(['GET', 'POST'])
def editor_dashboard(request):
    product_req = Product_Request.objects.filter(user_id=1)
    return render(request, 'editor_dashboard.html', {'products': product_req}) 

