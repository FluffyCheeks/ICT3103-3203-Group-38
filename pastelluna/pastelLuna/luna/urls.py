from django.urls import path
from . import views

urlpatterns = [
     path("", views.home, name="home"),
     path("home", views.home, name="home"),
     path("profile", views.profile, name="profile"),
     path('products', views.retrieve_product, name="products"),
     path('products/<int:pk>', views.retrieve_product_details,name="products_details"),
     path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),

]

