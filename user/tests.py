from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserApiTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("user:register")
        self.token_url = reverse("user:token")
        self.me_url = reverse("user:profile")

        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongPassword123!",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user_success(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password123!",
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertTrue(
            User.objects.filter(email=payload["email"]).exists()
        )

    def test_register_user_duplicate_email_fails(self):
        payload = {
            "username": "anotheruser",
            "email": self.user_data["email"],
            "password": "Password123!",
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_success(self):
        payload = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.token_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_invalid_credentials_fails(self):
        payload = {
            "username": self.user_data["username"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.token_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_me_unauthorized_fails(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_me_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
