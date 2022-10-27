from django.shortcuts import redirect, render
from .models import *

#Testing out http
from django.http import HttpResponse

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
        # user = authenticate(request, email=email, password=password)
        exist_username = Users.objects.filter(email=email).exists()
        exist_password = Users.objects.filter(password=password).exists()

        if exist_username:
            someuser = Users.objects.get(email__contains=email)
            if someuser.password == password:
                if someuser is not None:
                    #login(request, user)
                    cookie_session(request)
                    return render(request, "profile.html")
            else:
                msg = "Wrong email or password"
                #form = AuthenticationForm(request.POST)
                return render(request, 'login.html', {'msg': msg})
        else:
            msg = "Wrong email or password"
            #form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'msg': msg})
    else:
        #form = AuthenticationForm()
        return render(request, "login.html")

def cookie_session(request):
    request.session.set_test_cookie()
    print("I am line 72")

def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        print("I am line 77")
        response = HttpResponse("dataflair<br> cookie created")
    else:
        print("I am line 80")
        response = HttpResponse("Dataflair <br> Your browser does not accept cookies")
    return response

def logoutpage(request):
    print("Here")
    request.session.flush()
    if request.session.test_cookie_worked():
        cookie_delete(request)
        print("Or Here")
        return render(request, "profile.html")
    return render(request, "home.html")