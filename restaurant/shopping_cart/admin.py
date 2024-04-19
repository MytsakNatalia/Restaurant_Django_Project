from django.contrib import admin
from shopping_cart.models import ShoppingCart, ShoppingCartItem, Order
# Register your models here.
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Order)