# myapp/tests.py

from django.test import TestCase
from django.urls import reverse
from myapp.models import CustomUser

class SimpleTestCase(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user = CustomUser.objects.create_user(email="test@example.com", password="Test123!")
        self.assertEqual(user.email, "test@example.com")