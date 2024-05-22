from decimal import Decimal
from django.test import TestCase, SimpleTestCase
from menu.models import *


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name='Test Product', prod_weight_gram=500, prod_price=15.99)

    def test_name_content(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.name}'
        self.assertEquals(expected_object_name, 'Test Product')

    def test_prod_weight_gram_content(self):
        product = Product.objects.get(id=1)
        expected_object_weight = product.prod_weight_gram
        self.assertEquals(expected_object_weight, 500)

    def test_prod_price_content(self):
        product = Product.objects.get(id=1)
        expected_object_price = product.prod_price
        self.assertEquals(expected_object_price, Decimal('15.99'))


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category')

    def test_name_content(self):
        category = Category.objects.get(id=1) 
        expected_object_name = f'{category.name}'
        self.assertEquals(expected_object_name, 'Test Category')


class MealModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category')
        Meal.objects.create(name='Test Meal', weight=300, price=12.50, category=category, is_vegan=True, is_spicy=False)

    def test_name_content(self):
        meal = Meal.objects.get(id=1)
        expected_object_name = f'{meal.name}'
        self.assertEquals(expected_object_name, 'Test Meal')
    
    def test_weight_content(self):
        meal = Meal.objects.get(id=1)
        expected_object_weight = meal.weight
        self.assertEquals(expected_object_weight, 300)

    def test_price_content(self):
        meal = Meal.objects.get(id=1)
        expected_object_price = meal.price
        self.assertEquals(expected_object_price, Decimal('12.50'))

    def test_category_content(self):
        meal = Meal.objects.get(id=1)
        expected_object_category = meal.category
        self.assertEquals(expected_object_category, Category.objects.get(id=1))

    def test_is_vegan_content(self):
        meal = Meal.objects.get(id=1)
        expected_object_is_vegan = meal.is_vegan
        self.assertEquals(expected_object_is_vegan, True)

    def test_is_spicy_content(self):
        meal = Meal.objects.get(id=1)
        expected_object_is_spicy = meal.is_spicy
        self.assertEquals(expected_object_is_spicy, False)

class MealProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category')
        meal = Meal.objects.create(
            name='Test Meal',
            weight=300,
            price='12.50',
            category=category,
            is_vegan=True,
            is_spicy=False
        )
        product = Product.objects.create(
            name='Test Product',
            prod_weight_gram=500,
            prod_price='15.99'
        )
        MealProduct.objects.create(
            meal=meal,
            product=product,
            prod_amount=2
        )

    def test_str_method(self):
        meal_product = MealProduct.objects.get(id=1)
        expected_object_name = f'{meal_product.meal.name} - {meal_product.product.name}'
        self.assertEquals(expected_object_name, 'Test Meal - Test Product')

    def test_meal_content(self):
        meal_product = MealProduct.objects.get(id=1)
        expected_meal = meal_product.meal
        self.assertEquals(expected_meal, Meal.objects.get(id=1))

    def test_product_content(self):
        meal_product = MealProduct.objects.get(id=1)
        expected_product = meal_product.product
        self.assertEquals(expected_product, Product.objects.get(id=1))

    def test_prod_amount_content(self):
        meal_product = MealProduct.objects.get(id=1)
        expected_prod_amount = meal_product.prod_amount
        self.assertEquals(expected_prod_amount, 2)