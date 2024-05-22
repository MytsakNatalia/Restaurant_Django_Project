from django.urls import path
from menu.views import *
from users.views import *
from reservations.views import *

app_name = 'menu'

urlpatterns = [
    path('', index, name='index'),            
    path('category/<int:category_id>/', index, name='category'),  
    path('details/<int:meal_id>/', meal_detail, name='meal_detail'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),    
]