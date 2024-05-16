from django.test import  TestCase, Client, RequestFactory
from django.urls import reverse
from users.models import User
import  json
from django.http import  HttpResponseRedirect
from  users.views import login, logout
from     users.forms import UserLoginForm
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        #self.factory = RequestFactory()
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

    def test_login_POST_valid_credentials(self):
        # Prepare valid form data
        form_data = {
            'username': 'testuser',
            'password': '12345',
        }

        # Send a POST request to the login view with valid form data
        response = self.client.post(reverse('users:login'), data=form_data)

        # Assert that the response redirects to the index page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('menu:index'))

    def test_login_POST_invalid_credentials(self):
        # Prepare invalid form data (incorrect password)
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        # Send a POST request to the login view with invalid form data
        response = self.client.post(reverse('users:login'), data=form_data)

        # Assert that the response renders the login page again
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_register_GET(self):

        response = self.client.get(reverse('users:registration'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_registration_POST_valid_data(self):
        # Prepare valid form data
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser1',
            'email': 'test@example.com',
            'password1': '!Password123',
            'password2': '!Password123',
        }


        response = self.client.post(reverse('users:registration'), data=form_data)

        # Check if the user is created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertEqual(response.url, reverse('users:login'))

    def test_registration_POST_invalid_data(self):
        #  invalid form data (missing required fields)
        form_data = {
            'first_name': 'John',
            'last_name': '',  # Missing last name
            'username': 'testuser1',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }

        response = self.client.post(reverse('users:registration'), data=form_data)

        # Check if the user is not created in the database
        self.assertFalse(User.objects.filter(username='testuser1').exists())

        # Check the response
        self.assertEqual(response.status_code, 200)  # Should stay on registration page
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


