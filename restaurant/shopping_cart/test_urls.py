from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shopping_cart.views import (
    view_cart, add_to_cart, remove_from_cart,
    change_quantity, create_order, view_orders,
    cancel_order
)

class TestUrls(SimpleTestCase):
    def test_view_cart_url_resolves(self):
        url = reverse('shopping_cart:view_cart')
        self.assertEquals(resolve(url).func, view_cart)

    def test_add_to_cart_url_resolves(self):
        url = reverse('shopping_cart:add_to_cart', args=[1])  # Replace 1 with a valid meal_id
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_remove_from_cart_url_resolves(self):
        url = reverse('shopping_cart:remove_from_cart', args=[1])  # Replace 1 with a valid meal_id
        self.assertEquals(resolve(url).func, remove_from_cart)

    def test_change_quantity_url_resolves(self):
        url = reverse('shopping_cart:change_quantity', args=[1])  # Replace 1 with a valid meal_id
        self.assertEquals(resolve(url).func, change_quantity)

    def test_create_order_url_resolves(self):
        url = reverse('shopping_cart:create_order')
        self.assertEquals(resolve(url).func, create_order)

    def test_view_orders_url_resolves(self):
        url = reverse('shopping_cart:view_orders')
        self.assertEquals(resolve(url).func, view_orders)

    def test_cancel_order_url_resolves(self):
        url = reverse('shopping_cart:cancel_order', args=[1])  # Replace 1 with a valid order_id
        self.assertEquals(resolve(url).func, cancel_order)
