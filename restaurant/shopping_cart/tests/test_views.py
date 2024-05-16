from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from shopping_cart.views import create_order, calculate_total_price, view_orders, cancel_order
from users.models import User
from shopping_cart.models import ShoppingCart, ShoppingCartItem, Meal,  Order
from shopping_cart.forms import OrderForm
from menu.models import Category
from django.urls import reverse

class ShoppingCartViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.meal = Meal.objects.create(name='Test Meal', price=10.00, category=self.category)
        self.shopping_cart = ShoppingCart.objects.create(user=self.user)

    def test_view_cart(self):
        response = self.client.get(reverse('shopping_cart:view_cart'))
        self.assertEqual(response.status_code, 200)  # Assuming view_cart returns HTTP 200 on success

    def test_add_to_cart(self):
      #  meal = Meal.objects.create(name='Test Meal', price=10.00)
        response = self.client.post(reverse('shopping_cart:add_to_cart', kwargs={'meal_id': self.meal.id}))
        self.assertEqual(response.status_code, 302)

    def test_remove_from_cart(self):
        # Add meal to the cart
        self.client.post(reverse('shopping_cart:add_to_cart', kwargs={'meal_id': self.meal.id}))
        # Remove meal from the cart
        response = self.client.post(reverse('shopping_cart:remove_from_cart', kwargs={'meal_id': self.meal.id}))
        self.assertEqual(response.status_code, 302)  # Assuming remove_from_cart redirects to the cart view

    def test_change_quantity(self):
        # Add meal to the cart
        self.client.post(reverse('shopping_cart:add_to_cart', kwargs={'meal_id': self.meal.id}))
        # Change quantity of meal in the cart
        response = self.client.get(reverse('shopping_cart:change_quantity', kwargs={'meal_id': self.meal.id}), {'quantity': 2})
        self.assertEqual(response.status_code, 302)



class CreateOrderViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        login_data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(reverse('users:login'), login_data)
       # self.client.login(username='testuser', password='password')
        self.shopping_cart = ShoppingCart.objects.get(user=self.user, is_active=True)

    def test_get_method(self):
        request = self.factory.get(reverse('shopping_cart:create_order'))
        request.user = self.user
        response = create_order(request)
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        form_data = {
            'address': 'Test Address',
            'total_price': 100.00
        }
        request = self.factory.post(reverse('shopping_cart:create_order'), form_data)
        request.user = self.user


        response = create_order(request)


        self.assertEqual(response.status_code, 302)


        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 1)  # Ensure only one order is created
        order = orders.first()
        self.assertEqual(order.address, form_data['address'])  # Check address
       # self.assertEqual(order.total_price, form_data['total_price'])  # Check total price
        current_cart = new_shopping_cart = ShoppingCart.objects.get(user=self.user, id=self.shopping_cart.id)
        self.assertEqual(order.shopping_cart.id, self.shopping_cart.id)  # Check shopping cart association

        self.assertFalse(current_cart.is_active)  # Ensure shopping cart is deactivated

        # Check that a new active shopping cart is created
        new_shopping_cart = ShoppingCart.objects.get(user=self.user, is_active=True)
        self.assertIsNotNone(new_shopping_cart)  # Ensure new shopping cart is created

        order.delete()
        new_shopping_cart.delete()




class OrderViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')

        # Create a shopping cart for the user
        self.shopping_cart = ShoppingCart.objects.create(user=self.user, is_active=True)

        # Create some shopping cart items for testing
        self.meal1 = Meal.objects.create(name='Meal 1', price=10)
        self.meal2 = Meal.objects.create(name='Meal 2', price=15)
        self.item1 = ShoppingCartItem.objects.create(shopping_cart=self.shopping_cart, meal=self.meal1, quantity=2)
        self.item2 = ShoppingCartItem.objects.create(shopping_cart=self.shopping_cart, meal=self.meal2, quantity=1)

        # Create an order for the user
        self.order = Order.objects.create(user=self.user, total_price=0)  # Assuming the initial total price is 0

    def test_calculate_total_price(self):
        total_price = calculate_total_price(self.shopping_cart)
        expected_price = 10 * 2 + 15 * 1  # Total price of items in the shopping cart
        self.assertEqual(total_price, expected_price)

    def test_view_orders(self):
        request = HttpRequest()
        request.user = self.user

        response = view_orders(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_cart/view_orders.html')
        self.assertIn('orders', response.context)
        self.assertQuerysetEqual(response.context['orders'], Order.objects.filter(user=self.user))

    def test_cancel_order(self):
        request = HttpRequest()
        request.META['HTTP_REFERER'] = '/index/'  # Simulate the HTTP_REFERER header

        # Cancel the order
        cancel_order(request, self.order.id)

        # Retrieve the updated order from the database
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, Order.CANCELED)

        # Assert redirection to the previous page after canceling the order
        self.assertEqual(cancel_order(request, self.order.id).url, '/index/')