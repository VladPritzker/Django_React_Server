from django.test import SimpleTestCase
from django.urls import reverse, resolve
from myapp.views.user_views import register_user, simple_login
from myapp.views.password_reset.password_reset import reset_password_form, reset_password, request_password_reset
from myapp.views.plaid.plaid_views import create_link_token, get_access_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class TestUrls(SimpleTestCase):

    def test_homepage_url(self):
        url = reverse('homepage')
        self.assertEqual(resolve(url).view_name, 'homepage')

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register_user)

    def test_simple_login_url(self):
        url = reverse('simple_login')
        self.assertEqual(resolve(url).func, simple_login)

    def test_token_obtain_pair_url(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_create_link_token_url(self):
        url = reverse('create_link_token')
        self.assertEqual(resolve(url).func, create_link_token)

    def test_get_access_token_url(self):
        url = reverse('get_access_token')
        self.assertEqual(resolve(url).func, get_access_token)

    def test_reset_password_form_url(self):
        url = reverse('reset_password_form')
        self.assertEqual(resolve(url).func, reset_password_form)

    def test_reset_password_submit_url(self):
        url = reverse('reset_password')
        self.assertEqual(resolve(url).func, reset_password)

    def test_request_password_reset_url(self):
        url = reverse('request_password_reset')
        self.assertEqual(resolve(url).func, request_password_reset)
