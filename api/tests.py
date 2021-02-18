from django.test import TestCase
from accounts.models import User
from rest_framework import status
from rest_framework.test import (
    APIClient
)

class UserTest(TestCase):
    """
    This are the test related to the User
    """
    def setUp(self):
        self.client = APIClient()
        user = User()
        user.email = 'test@222.com'
        user.set_password('andjadjaskjd')
        user.save()

    def test_registration_ok(self):
        url = '/api/v1/accounts/registration/'
        data = {
            'email': 'test@test.com',
            'password1': '1234idu32iu32',
            'password2': '1234idu32iu32',
        }
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_registration_fail(self):
        url = '/api/v1/accounts/registration/'
        data = {
            'email': 'test@test.com',
            'password2': '1234idu32iu32',
        }
        response = self.client.post(url, data=data)
        res_text = response.json().get('password1')[0]
        self.assertEquals(res_text, 'This field is required.')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_ok(self):
        url = '/api/v1/accounts/login/'
        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        url = '/api/v1/accounts/login/'
        data = {
            'email': 'test@test.com',
            'password': '1234iasdsaddu32iu32',
        }
        response = self.client.post(url, data=data)
        res_text= response.json().get('non_field_errors')[0]
        self.assertEquals(res_text, 'Unable to log in with provided credentials.')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)