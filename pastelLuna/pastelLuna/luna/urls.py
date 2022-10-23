from django.urls import path
from . import views

urlpatterns = [
     path("", views.home, name="home"),
     path("home", views.home, name="home"),
     path("profile", views.profile, name="profile"),
     path("registration",views.registration, name="registation"), #added this
     path("shop", views.shop, name="shop"),
     path('<slug:slug>', views.retrieve_product_details,name="product_details"),
     path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
     # path('editor_dash', views.editor_dashboard, name="editor_dashboard"),
]

