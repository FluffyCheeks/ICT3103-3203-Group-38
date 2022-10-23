from django.urls import path

from .views.profile import profile
from .views.product_details import retrieve_product_details
from .views.home import shop, home
from .views.user import registration, editor_dash


urlpatterns = [
     path("", home, name="home"),
     path("home", home, name="home"),
     path("profile", profile, name="profile"),
     path("registration",registration, name="registation"), #added this
     path("shop", shop, name="shop"),
     path('<slug:slug>', retrieve_product_details,name="product_details"),
     path('editor_dash', editor_dash, name="editor_dashboard"),
]

