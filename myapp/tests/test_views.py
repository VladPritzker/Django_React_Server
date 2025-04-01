import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from myapp.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='apitest',
            email='apitest@example.com',
            password='securepass123'
        )

    def test_simple_login(self):
        url = reverse('simple_login')
        data = {'email': 'apitest@example.com', 'password': 'securepass123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Manually parse JSON from response.content
        json_response = json.loads(response.content)
        self.assertIn('access', json_response)
        self.assertEqual(json_response['email'], 'apitest@example.com')

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_response = json.loads(response.content)
        self.assertEqual(json_response['message'], 'User registered successfully')

    def test_get_user_data(self):
        url = reverse('users_data', kwargs={'user_id': self.user.id})
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
        response = self.client.get(url)
  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(json_response['username'], 'apitest')

    def test_patch_user_data(self):
        url = reverse('users_data', kwargs={'user_id': self.user.id})
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
        data = {'username': 'updateduser'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        self.assertEqual(json_response['user']['username'], 'updateduser')
