from django.db import models
from users.models import User
# Create your models here.
class ShoppingCart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(to=ShoppingCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)


