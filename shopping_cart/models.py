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


class Order(models.Model):
    WAITING = 'Waiting for processing'
    IN_PROCESS = 'In process'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
    DECLINED = 'Declined'

    STATUS_CHOICES = [
        (WAITING, 'Waiting for processing'),
        (IN_PROCESS, 'In process'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
        (DECLINED, 'Declined'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=256)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    shopping_cart = models.ForeignKey(to=ShoppingCart, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WAITING)

