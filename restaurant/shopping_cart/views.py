from django.shortcuts import render, redirect
from  .models import ShoppingCart, ShoppingCartItem
from menu.models import Meal
from .forms import OrderForm
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

def change_quantity(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    user_cart = ShoppingCart.objects.get(user=request.user, is_active=True)
    meal_cart_item = ShoppingCartItem.objects.get(shopping_cart=user_cart, meal=meal)
    new_quantity = int(request.GET.get('quantity', 0))
    meal_cart_item.quantity = new_quantity
    meal_cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'shopping_cart/view_cart'))

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            user_cart = ShoppingCart.objects.get(user=request.user, is_active=True)
            order.shopping_cart = user_cart
            order.total_price = calculate_total_price(user_cart)
            order.save()
            return redirect('menu/index')
    else:
        form = OrderForm()
        form.fields['total_price'].initial = calculate_total_price()
    return render(request, 'order/create.html', {'form': form})

def calculate_total_price(cart):
    total_price = 0
    shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=cart)
    for item in shopping_cart_items:
        total_price += item.total_price
    return total_price



