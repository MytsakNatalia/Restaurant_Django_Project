from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Meal, Category

class TestViewsMenu(TestCase):
    def setUp(self):
        # Create a Category object for testing
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')

        # Create a Meal object associated with the Category for testing
        self.meal = Meal.objects.create(
            name='Test Meal',
            weight=200,
            price=10.99,
            category=self.category,
            is_vegan=True,
            is_spicy=False,            
            image='meals_images/test_image.jpg'
        )
        
        self.meal_vegan_spicy = Meal.objects.create(
            name='Vegan Spicy Meal',
            weight=200,
            price=10.99,
            category=self.category,
            is_vegan=True,
            is_spicy=True,
            image='meals_images/test_image.jpg'
        )

        self.meal_vegan = Meal.objects.create(
            name='Vegan Meal',
            weight=200,
            price=10.99,
            category=self.category,
            is_vegan=True,
            is_spicy=False,
            image='meals_images/test_image.jpg'
        )

        self.meal_spicy = Meal.objects.create(
            name='Spicy Meal',
            weight=200,
            price=10.99,
            category=self.category,
            is_vegan=False,
            is_spicy=True,
            image='meals_images/test_image.jpg'
        )

    
    def test_index_view(self):
        response = self.client.get(reverse('menu:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/index.html')
        self.assertContains(response, 'Test Meal')
        
    def test_index_view_with_category(self):
        response = self.client.get(reverse('menu:category', kwargs={'category_id': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/index.html')
        self.assertContains(response, 'Test Meal')     

    def test_index_view_with_spicy_filter(self):
        response = self.client.get(reverse('menu:index') + '?spicy=true')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/index.html')
        self.assertNotContains(response, 'Vegan Meal')
        self.assertContains(response, 'Spicy Meal')
        self.assertContains(response, 'Vegan Spicy Meal')
                
    def test_meal_detail_view(self):
        response = self.client.get(reverse('menu:meal_detail', kwargs={'meal_id': self.meal.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/meal_detail.html')
        self.assertContains(response, 'Test Meal')