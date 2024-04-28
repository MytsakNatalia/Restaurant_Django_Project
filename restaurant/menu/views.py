from django.shortcuts import render, HttpResponse
from menu.models import Category, Meal, Product, MealProduct

def index(request):
    context = {
        'title': 'Menu',
        'categories': Category.objects.all(), 
        'meals': Meal.objects.all(),
    }
    return render(request, 'menu/index.html', context)

def meals(request):
    context = {
        'title': 'List of meals',
        'categories': Category.objects.all(), 
        'meals': Meal.objects.all(),
    }
    return render (request, 'menu/meals.html', context)

