from django.urls import path
from . import views
from . import cart
from . import checkout
from . import orderdetail

urlpatterns = [
     path("", views.home, name="home"),
     path("home", views.home, name="home"),
     path("profile", views.profile, name="profile"),
     path('products', views.retrieve_product, name="products"),
     path("registration",views.registration, name="registation"), #added this
     path("shop", views.shop, name="shop"),
     path('products/<int:pk>', views.retrieve_product_details,name="products_details"),
     path("cart", cart.viewcart, name="cart"),
     path("update-cart", cart.updatecart, name="updatecart"),
     path("delete-cart-item", cart.deletecartitem, name="deletecartitem"),
     path ('checkout', checkout.checkout, name="checkout"),
     path ('place-order', checkout.placeorder, name="placeorder"),
     path ('orderdetail', orderdetail.orderdetail, name="orderdetail"),
]

