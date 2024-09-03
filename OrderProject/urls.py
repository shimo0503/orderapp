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
from django.urls import path
from OrderApp.views import frontpage, append_menu, restcheck, restregister, create_order, addorder, provided, unprovided,provideflow, pay, payflow, payreverse, payreverseflow, restore_csv, minus_order, csv_install

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',frontpage, name = 'front'),
    path('restcheck/',restcheck, name = 'restcheck'),
    path('append_menu/',append_menu, name = 'append_menu'),
    path('restregister/',restregister, name = 'restregister'),
    path('neworder/', create_order, name = 'neworder'),
    path('addorder/', addorder, name = 'addorder'),
    path('provided/', provided, name = 'provided'),
    path('unprovided/', unprovided, name = 'unprovided'),
    path('provideflow/<int:pk>', provideflow, name = 'provideflow'),
    path('pay/', pay, name = 'pay'),
    path('payflow/<int:pk>', payflow, name = 'payflow'),
    path('payreverse/', payreverse, name = 'payreverse'),
    path('payreverseflow/<int:pk>', payreverseflow, name = 'payreverseflow'),
    path('restore/', restore_csv, name = 'restore_csv'),
    path('minus_order/', minus_order, name = 'minus_order'),
    path('csv_install/<str:filename>', csv_install, name='csv_install'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
