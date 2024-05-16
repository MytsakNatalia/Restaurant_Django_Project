from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import registartion, login, logout, profile


class TestUrls(SimpleTestCase):
    def test_profile_url_is_resolved(self):
        url = reverse('users:profile')
        self.assertEquals(resolve(url).func, profile)

    def test_login_url_is_resolved(self):
        url = reverse('users:login')
        self.assertEquals(resolve(url).func, login)

    def test_register_url_is_resolved(self):
        url = reverse('users:registration')
        self.assertEquals(resolve(url).func, registartion)

    def test_logout_url_is_resolved(self):
        url = reverse('users:logout')
        self.assertEquals(resolve(url).func, logout)