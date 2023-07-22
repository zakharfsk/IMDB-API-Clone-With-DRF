from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "testcase@gmail.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123",
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="NewPassword@123")

    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123",
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_logout(self):
        self.test_login()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(reverse('logout'), {"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
