from django.test import TestCase
from myapp.serializers import UserSerializer
from myapp.models import User

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'serializeruser',
            'email': 'serializer@example.com',
            'password': 'serializer123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_serializer_valid_data(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], self.user_data['username'])
        self.assertEqual(serializer.data['email'], self.user_data['email'])

    def test_serializer_invalid_data(self):
        data = {'username': '', 'email': 'invalid'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('email', serializer.errors)