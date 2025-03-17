from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from myapp.models import User

class UserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='apitest',
            email='apitest@example.com',
            password='securepass123'
        )
        self.client.login(username='apitest', password='securepass123')

    def test_get_user_profile(self):
        url = reverse('user-profile', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'apitest')

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        data = {'email': 'apitest@example.com', 'password': 'securepass123'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)