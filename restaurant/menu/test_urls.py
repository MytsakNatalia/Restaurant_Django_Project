from django.test import TestCase
from django.urls import reverse, resolve
from menu.views import *
from users.views import *
  
class TestUrlsMenu(TestCase):      
    def setUp(self):
        # Create a Category object for testing
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
    
    def test_index_url_is_resolved(self):
        url = reverse('menu:index')
        self.assertEquals(resolve(url).func, index)
        
    def test_category_url_is_resolved(self):        
        url = reverse('menu:category', args=[self.category.pk])          
        self.assertEquals(resolve(url).func, index)
    
    def test_meal_detail_url_is_resolved(self):        
        url = reverse('menu:meal_detail', args=[self.meal.pk])          
        self.assertEquals(resolve(url).func, meal_detail)
        
    def test_profile_url_is_resolved(self):
        url = reverse('users:profile')
        self.assertEquals(resolve(url).func, profile)
    
    def test_logout_url_is_resolved(self):
        url = reverse('users:logout')
        self.assertEquals(resolve(url).func, logout)  
        
    
    """def test_category_url_is_resolved(self):
        url = reverse('menu:category', args=[1])  
        self.assertEquals(resolve(url).func, index)
    
    def test_meal_detail_url_is_resolved(self):
        url = reverse('menu:meal_detail', args=[1])  
        self.assertEquals(resolve(url).func, meal_detail)"""