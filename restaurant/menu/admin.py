from django.contrib import admin
from menu.models import Category, Product, Meal, MealProduct

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Meal)
admin.site.register(MealProduct)