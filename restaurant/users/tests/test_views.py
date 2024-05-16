from django.test import  TestCase, Client
from django.urls import reverse
from users.models import User
import  json
from django.http import  HttpResponseRedirect
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345', first_name='John', last_name='Doe', email='test@example.com')
        self.client.login(username='testuser', password='12345')
    def test_profile_GET(self):

        response = self.client.get(reverse('users:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_POST(self):
        #  initial user data
        initial_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'test@example.com'
        }

        modified_data = {
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        # Log in the test user
        self.client.login(username='testuser', password='password')

        # Send a POST request to update the user's profile
        response = self.client.post(reverse('users:profile'), modified_data)


        # Retrieve the updated user instance from the database
        updated_user = User.objects.get(username='testuser')

        # Assert that the user's profile is updated correctly
        self.assertEqual(updated_user.first_name, modified_data['first_name'])
        self.assertEqual(updated_user.last_name, modified_data['last_name'])
        self.assertEqual(updated_user.email, 'test@example.com')  # Email should not change

        # Assert that the response redirects to the correct URL (assuming HttpResponseRedirect is used)
        self.assertRedirects(response, reverse('menu:index'))


    def test_login_GET(self):
        response = self.client.get(reverse('users:login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_profile_GET(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

