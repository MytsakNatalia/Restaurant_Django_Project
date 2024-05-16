from django.test import TestCase
from users.models import User
from users.forms import UserProfileForm, UserLoginForm, UserRegistrationForm

class TestUserLoginForm(TestCase):
    def test_valid_form_data(self):
        # Create a test user
        test_user = User.objects.create_user(username='testuser', password='password')


        form_data = {
            'username': 'testuser',
            'password': 'password',
        }


        form = UserLoginForm(data=form_data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):

        form_data = {}


        form = UserLoginForm(data=form_data)

        # Assert that the form is not valid
        self.assertFalse(form.is_valid())

class TestUserProfileForm(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')  # Use custom user model manager

    def test_valid_form_data(self):
        valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            # 'username' and 'email' are readonly fields and should not be included
        }
        form = UserProfileForm(instance=self.user, data=valid_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        invalid_data = {
            # 'first_name' and 'last_name' are required fields and are missing
        }
        form = UserProfileForm(instance=self.user, data=invalid_data)
        self.assertFalse(form.is_valid())


class TestUserRegistrationForm(TestCase):
    def test_valid_form_data(self):

        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password1': '!Password123',
            'password2': '!Password123',
        }


        form = UserRegistrationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        # Prepare invalid form data (missing required fields)
        form_data = {
            'first_name': 'John',
            'last_name': '',  # Missing last name
            'username': 'johndoe',
            'email': '',  # Missing email
            'password1': 'password123',
            'password2': '',  # Missing password confirmation
        }


        form = UserRegistrationForm(data=form_data)


        # Assert that the form is not valid
        self.assertFalse(form.is_valid())