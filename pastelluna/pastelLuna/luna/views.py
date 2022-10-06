from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
    # return render(request, 'home.html')
    return render(request, 'home.html')


@csrf_exempt
def profile(request):
    # inner join with id where user id =1 (pass in through param)
    obj = Users.objects.select_related("role_id").filter(id=1)

    if request.method == 'POST':
        if request.POST.get('save', '') == 'update':
            editProfile = Users.objects.get(id=1)
            editProfile.first_name = request.POST.get('firstname')
            editProfile.last_name = request.POST.get('lastname')
            editProfile.phone = request.POST.get('mobile')
            editProfile.address = request.POST.get("address")
            editProfile.allergies = request.POST.get("allergies")
            # Save to the database here
            editProfile.save()
            return HttpResponseRedirect(request.path_info)
    else:
        context = {"object": obj}
        return render(request, "profile.html", context)
