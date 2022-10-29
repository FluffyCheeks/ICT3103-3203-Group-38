from django.urls import path

from .views.profile import profile
from .views.product_details import retrieve_product_details
from .views.home import shop, home
from .views.registration import registration
from .views.admin_dashboard import admin_dashboard
from .views.home import shop, home, showcart_base
from .views.user import editor_dashboard

from .views.checkout import checkout, placeorder
from .views.orderdetail import orderdetail
from .views.cart import viewcart, updatecart, deletecartitem

from .views.user import editor_dashboard
from .views.registration import registration
from .views.admin_dashboard import admin_dashboard
from .views.home import shop, home, showcart_base

from .views.loginpage import loginpage
from .views.logoutpage import logoutpage






urlpatterns = [

     path("", home, name="home"),
     path("home", home, name="home"),
     path("profile", profile, name="profile"),
     path("registration",registration, name="registation"), #added this
     path("shop", shop, name="shop"),
     path('admin_dashboard', admin_dashboard, name="admin_dashboard"),
     path("editor_dashboard", editor_dashboard, name="editor_dashboard"),
     path("cart", viewcart, name="cart"),
     path("update-cart", updatecart, name="updatecart"),
     path("delete-cart-item", deletecartitem, name="deletecartitem"),
     path ('checkout', checkout, name="checkout"),
     path ('placeorder', placeorder, name="placeorder"),
     path ('orderdetail', orderdetail, name="orderdetail"),
     path("loginpage", loginpage, name="loginpage"),
     path("logout", logoutpage, name="home"),
     path('<slug:slug>', retrieve_product_details,name="product_details"),
    

]

