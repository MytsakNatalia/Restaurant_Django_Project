from django.shortcuts import render,  get_object_or_404
from menu.models import Category, Meal, Product, MealProduct

def index(request):
    categories = Category.objects.all()  
    meals = Meal.objects.all()  

    context = {
        'title': 'Menu',
        'categories': categories, 
        'meals': meals,
    }
    return render(request, 'menu/index.html', context)

def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id)
    categories = Category.objects.all() 
    context = {
        'title': meal.name,
        'categories': categories,
        'meal': meal,
    }
    return render(request, 'menu/meal_detail.html', context)

