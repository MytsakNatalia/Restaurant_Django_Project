from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    prod_weight_gram = models.PositiveIntegerField(default=0)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    is_vegan = models.BooleanField(default=False)
    is_spicy = models.BooleanField(default=False)
    image = models.ImageField(upload_to='meals_images')

    def __str__(self):
        return self.name

class MealProduct(models.Model):
    meal = models.ForeignKey(to=Meal, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    prod_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.meal.name} - {self.product.name}"		