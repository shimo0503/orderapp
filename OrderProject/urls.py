"""
URL configuration for OrderProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from OrderApp.views import ProductAPIView, RestRegister, NewMenu, NewOrder, AddOrder, CustomerAPIView, DeleteMenu, Provide, Pay
from accounts.forms import CustomLoginForm
from accounts.views import custom_login
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/product', ProductAPIView.as_view(), name = 'prod'),
    path('api/customer', CustomerAPIView.as_view(), name = 'customer'),
    path('api/rest', RestRegister.as_view(), name='rest'),
    path('api/Menu/new', NewMenu.as_view(), name = 'newmenu'),
    path('api/Menu/delete', DeleteMenu.as_view(), name = 'deletemenu'),
    path('api/order/new', NewOrder.as_view(), name = 'neworder'),
    path('api/order/add', AddOrder.as_view(), name = 'neworder'),
    path('api/provide', Provide.as_view(), name = 'provide'),
    path('api/pay', Pay.as_view(), name = 'pay'),
]
