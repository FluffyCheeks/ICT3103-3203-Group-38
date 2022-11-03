from django.urls import path
from django.views.generic import RedirectView

from .views.profile import profile
from .views.product_details import retrieve_product_details
from .views.checkout import checkout, placeorder
from .views.orderdetail import orderdetail
from .views.cart import viewcart, updatecart, deletecartitem
from .views.user import editor_dashboard
from .views.registration import registration
from .views.registration_success import registration_success
from .views.admin_dashboard import admin_dashboard
from .views.home import shop, home
from .views.loginpage import loginpage
from .views.resetpassword import resetpassword
from .views.logoutpage import logoutpage
from .views.aboutus import aboutus

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
     # path(route, view, kwargs=None, name=None) << syntax 

     path("", home, name="home"),
     path("home", home, name="home"),
     path("home", home, name="home_aft_login"),
     path("profile", profile, name="profile"),
     path("registration",registration, name="registration"), #added this
     path("registration_success",registration_success, name="registration_success"), #added this 01 Nov 22
     path("'<str:email>/'", registration_success, name="registration_success"),  # added this 01 Nov 22
     path("shop", shop, name="shop"),
     path('admin_dashboard', admin_dashboard, name="admin_dashboard"),
     path("editor_dashboard", editor_dashboard, name="editor_dashboard"),
     path("aboutus", aboutus, name="aboutus"),
     path("cart", viewcart, name="cart"),
     path("update-cart", updatecart, name="updatecart"),
     path("delete-cart-item", deletecartitem, name="deletecartitem"),
     path("resetpassword", resetpassword, name="resetpassword"),
     path ('checkout', checkout, name="checkout"),
     path ('placeorder', placeorder, name="placeorder"),
     path ('orderdetail', orderdetail, name="orderdetail"),
     path("loginpage", loginpage, name="loginpage"),
     path("logoutpage", logoutpage, name="home"),
     path('<slug:slug>', retrieve_product_details,name="product_details"),
    

]
