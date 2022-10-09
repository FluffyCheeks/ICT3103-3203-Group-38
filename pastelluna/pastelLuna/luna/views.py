import email
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


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

def loginpage(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile')
        else:
            msg = user
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html")

"""        
        obj1 = Users.objects.select_related("password")
        context = {"object": obj}
        if email == obj:
            return render(request, "home.html")
        else:
            return render(request, "login.html", context)
"""

'''
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = user.object.get(username=username)
        except:
            messages.error(request, 'User doesn not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {}
    return render(request, "registration\login.html", context)
'''