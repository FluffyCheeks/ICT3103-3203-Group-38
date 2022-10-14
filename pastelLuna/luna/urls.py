from django.urls import path
from . import views

urlpatterns = [
     path("", views.home, name="home"),
     path("home", views.home, name="home"),
     path("profile", views.profile, name="profile"),
     path('products', views.retrieve_product, name="products"),
     path("registration",views.registration, name="registation"), #added this
     path("shop", views.shop, name="shop"),
     path('products/<int:pk>', views.retrieve_product_details,name="products_details"),
]

