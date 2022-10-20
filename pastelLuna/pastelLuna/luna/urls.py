from django.urls import path
from . import views

urlpatterns = [
     path("", views.home, name="home"),
     path("home", views.home, name="home"),
     path("profile", views.profile, name="profile"),
     path('products', views.retrieve_product, name="products"),
     path("registration",views.registration, name="registation"), #added this
     path("shop", views.shop, name="shop"),
     path('products/<slug:slug>', views.retrieve_product_details,name="product_details"),
     # path('editor_dash', views.editor_dashboard, name="editor_dashboard"),
]

