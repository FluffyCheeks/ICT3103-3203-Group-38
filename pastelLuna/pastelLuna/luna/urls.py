from django.urls import path

from .views.profile import profile
from .views.product_details import retrieve_product_details
from .views.home import shop, home
from .views.registration import registration
from .views.admin_dashboard import admin_dashboard
from .views.home import shop, home, showcart_base
from .views.user import editor_dashboard

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

     path("", home, name="home"),
     path("home", home, name="home"),
     path("profile", profile, name="profile"),
     path("registration",registration, name="registation"), #added this
     path("shop", shop, name="shop"),
     path('admin_dashboard', admin_dashboard, name="admin_dashboard"),
     path("editor_dashboard", editor_dashboard, name="editor_dashboard"),
     path('<slug:slug>', retrieve_product_details,name="product_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

