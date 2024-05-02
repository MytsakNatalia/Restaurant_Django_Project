from django.urls import path, include
from .views import view_cart, add_to_cart
app_name = 'shopping_cart'
urlpatterns= [
    path('view_cart', view_cart, name='view_cart'),
    path('add_to_cart/<int:meal_id>/', add_to_cart, name='add_to_cart'),
]