from django.urls import path, include
from .views import view_cart, add_to_cart, remove_from_cart, change_quantity, create_order
app_name = 'shopping_cart'
urlpatterns= [
    path('view_cart', view_cart, name='view_cart'),
    path('add_to_cart/<int:meal_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:meal_id>/', remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<int:meal_id>/', change_quantity, name='change_quantity'),
    path('create_order/', create_order, name='create_order')
    ]