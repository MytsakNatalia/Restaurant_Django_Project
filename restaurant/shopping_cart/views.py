from django.shortcuts import render, redirect
from  .models import ShoppingCart, ShoppingCartItem
from menu.models import Meal
# Create your views here.
def view_cart(request):
    user_cart = ShoppingCart.objects.get(user=request.user, is_active = True)
    cart_items = ShoppingCartItem.objects.filter(shopping_cart = user_cart)

    context = {
        'shopping_cart': user_cart,
        'cart_items': cart_items
    }
    return render(request, 'shopping_cart/view_cart.html', context)

def add_to_cart(request, meal_id):
    meal = Meal.objects.get(id = meal_id)
    user_cart = ShoppingCart.objects.get(user=request.user, is_active=True)
    meal_cart_items = ShoppingCartItem.objects.filter(shopping_cart= user_cart, meal= meal)
    if not meal_cart_items.exists():
        ShoppingCartItem.objects.create(shopping_cart=user_cart, meal=meal, quantity=1, total_price=meal.price)
    else:
        cart_item = meal_cart_items.first()
        cart_item.quantity +=1
        cart_item.total_price = cart_item.quantity*cart_item.meal.price
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'menu/'))

def remove_from_cart(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    user_cart = ShoppingCart.objects.get(user=request.user, is_active=True)
    meal_cart_item = ShoppingCartItem.objects.get(shopping_cart=user_cart, meal=meal)
    meal_cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'shopping_cart/view_cart'))

def change_quantity(request, meal_id, quantity):
    meal = Meal.objects.get(id=meal_id)
    user_cart = ShoppingCart.objects.get(user=request.user, is_active=True)
    meal_cart_item = ShoppingCartItem.objects.get(shopping_cart=user_cart, meal=meal)
    meal_cart_item.quantity = quantity
    meal_cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'shopping_cart/view_cart'))


