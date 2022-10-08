from django.shortcuts import render
from luna.serializers import ProductSerializer
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .models import *

def home(request):
    """View function for home page of site."""

    # # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()

    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # # The 'all()' is implied by default.
    # num_authors = Author.objects.count()

    # context = {
    #     'num_books': num_books,
    #     'num_instances': num_instances,
    #     'num_instances_available': num_instances_available,
    #     'num_authors': num_authors,
    # }
    # context = {

    # }

    # Render the HTML template index.html with the data in the context variable
    # return render(request, 'home.html', context=context)
    #return render(request, 'home.html')
    return render(request, 'home.html')

def profile(request):
    # inner join with id where user id =1
    obj = Users.objects.select_related("role_id").filter(id=1)
    context = {"object": obj}
    return render(request, "profile.html", context)

@api_view(['GET'])
def retrieve_product(request):
    products = Product_Details.objects.all()
    context = {"object": products}
    product_serializer = ProductSerializer(products, many=True) 
    return JsonResponse(product_serializer.data, safe=False) 
    #return render(request, context)

@api_view(['GET'])
def retrieve_product_details(request, pk):
    product_Detail = Product_Details.objects.get(pk=pk)
    if request.method == 'GET': 
        product_serializer = ProductSerializer(product_Detail)
        return JsonResponse(product_serializer.data) 
    # obj = Users.objects.select_related("role_id").filter(id=pk)
    # context = {"object": obj}
    #return render(request, "profile.html", context)