from django.urls import path, include
from .views import view_cart, add_to_cart, remove_from_cart, change_quantity, create_order, view_orders, cancel_order
app_name = 'shopping_cart'

urlpatterns= [
    path('view_cart', view_cart, name='view_cart'),
    path('add_to_cart/<int:meal_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:meal_id>/', remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<int:meal_id>/', change_quantity, name='change_quantity'),
    path('create_order/', create_order, name='create_order'),
    path('view_orders/', view_orders, name='view_orders'),
   path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order')
    ]