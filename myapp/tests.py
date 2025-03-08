from django.test import TestCase
from myapp.models import User

class SimpleTestCase(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", password="Test123!")
        self.assertEqual(user.email, "test@example.com")