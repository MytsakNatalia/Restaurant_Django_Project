from django.test import TestCase
from shopping_cart.forms import OrderForm
from shopping_cart.models import Order

class TestOrderForm(TestCase):
    def test_order_form_valid(self):

        form_data = {
            'address': '123 Main St',
            'total_price': 100.00
        }


        form = OrderForm(data=form_data)


        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        #  invalid form data (missing address)
        form_data = {
            'total_price': 100.00
        }


        form = OrderForm(data=form_data)


        self.assertFalse(form.is_valid())

    def test_order_form_initialization(self):

        order = Order(address='456 Elm St', total_price=150.00)

        # Create form instance with the order instance
        form = OrderForm(instance=order)

        # Check if the form is initialized correctly
        self.assertEqual(form.initial['address'], '456 Elm St')
        self.assertEqual(form.initial['total_price'], 150.00)
