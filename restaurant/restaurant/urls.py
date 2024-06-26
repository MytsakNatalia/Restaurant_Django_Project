"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from menu.views import *
from users.views import *
from reservations.views import *
from django.conf.urls.static import static
from django.conf import settings
from users.views import login
from shopping_cart.views import view_cart, add_to_cart

urlpatterns = [
    path('', login, name='login'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path ('menu/', include('menu.urls', namespace='menu')),
    path('shopping_cart/', include('shopping_cart.urls', namespace='shopping_cart')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)