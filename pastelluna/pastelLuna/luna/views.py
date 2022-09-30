from django.shortcuts import render
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