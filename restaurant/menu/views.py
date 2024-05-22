from django.shortcuts import render,  get_object_or_404
from menu.models import Category, Meal, Product, MealProduct

def index(request, category_id=None):
    categories = Category.objects.all()
    meals = Meal.objects.all()
    
    if category_id:
        category = Category.objects.get(pk=category_id)
        meals = meals.filter(category=category)
    
    vegan = request.GET.get('vegan')
    if vegan:
        meals = meals.filter(is_vegan=True)
    
    spicy = request.GET.get('spicy')
    if spicy:
        meals = meals.filter(is_spicy=True)

    context = {
        'title': 'Menu',
        'categories': categories,
        'meals': meals,
        'selected_category_id': category_id,
        'vegan': vegan,
        'spicy': spicy 
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

