from django.test import SimpleTestCase
from django.urls import reverse, resolve
from myapp.views import UserProfileView, UserLoginView

class TestUrls(SimpleTestCase):
    def test_user_profile_url(self):
        url = reverse('user-profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_login_url(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)