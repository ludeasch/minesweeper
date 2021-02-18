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
        self.data_new = {
            'email': 'test@test.com',
            'username': 'test2',
            'password1': '1234idu32iu32',
            'password2': '1234idu32iu32',
        }
        user = User()
        user.email = 'test@222.com'
        user.username = 'testcom'
        user.set_password('andjadjaskjd')
        user.save()

    def test_registration_ok(self):
        # test the corect case og the registration
        url = '/api/v1/accounts/registration/'
        response = self.client.post(url, data=self.data_new)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.all().count(), 2)
        self.assertTrue(User.objects.filter(email='test@test.com').exists())


    def test_registration_fail(self):
         # test when the registration fail for a miss field
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
        # test the corect case of the login
        url = '/api/v1/accounts/login/'
        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))

    def test_login_fail(self):
         # test when the login fail for wrong credentials
        url = '/api/v1/accounts/login/'
        data = {
            'email': 'test@test.com',
            'password': '1234iasdsaddu32iu32',
        }
        response = self.client.post(url, data=data)
        res_text= response.json().get('non_field_errors')[0]
        self.assertEquals(res_text, 'Unable to log in with provided credentials.')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)