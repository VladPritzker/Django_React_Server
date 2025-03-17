from django.test import TestCase
from myapp.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword123'))
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'testuser')