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
        user.first_name = 'juan' 
        user.last_name = 'carlos'
        user.set_password('andjadjaskjd')
        user.save()
        
        self.url_login = '/api/v1/accounts/login/'
        self.url_registration = '/api/v1/accounts/registration/'
        self.url_get_user = '/api/v1/accounts/user/'
        self.url_change_password = '/api/v1/accounts/password/change/'

    def test_registration_ok(self):
        """
        Test the correct case of the registration
        """

        response = self.client.post(self.url_registration, data=self.data_new)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.all().count(), 2)
        self.assertTrue(User.objects.filter(email='test@test.com').exists())


    def test_registration_fail(self):
        """ 
        Test when the registration fail for a miss field
        """

        data = {
            'email': 'test@test.com',
            'password2': '1234idu32iu32',
        }
        response = self.client.post(self.url_registration, data=data)
        res_text = response.json().get('password1')[0]
        self.assertEquals(res_text, 'This field is required.')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_ok(self):
        """
        Test the correct case of the login
        """

        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        response = self.client.post(self.url_login, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))

    def test_login_fail(self):
        """
        Test when the login fail for wrong credentials
        """

        data = {
            'email': 'test@test.com',
            'password': '1234iasdsaddu32iu32',
        }
        response = self.client.post(self.url_login, data=data)
        res_text= response.json().get('non_field_errors')[0]
        self.assertEquals(res_text, 'Unable to log in with provided credentials.')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_ok(self):
        """
        Test the correct case of change password
        """

        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        data_p = {
            'new_password1': 'roberto12345',
            'new_password2': 'roberto12345'
        }
        #login
        response = self.client.post(self.url_login, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))
        # change password
        res_change = self.client.post(self.url_change_password, data=data_p)
        self.assertEquals(res_change.status_code, status.HTTP_200_OK)
        self.assertEquals(res_change.data.get('detail'), "New password has been saved.")

    def test_change_password_fail(self):
        """
        Test the change password with wrong data
        """

        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        data_p = {
            'new_password1': 'roberto12345',
            'new_password2': 'asdasdsadasdas'
        }
        # login
        response = self.client.post(self.url_login, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))
        # change password
        res_change = self.client.post(self.url_change_password, data=data_p)
        self.assertEquals(res_change.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(res_change.json().get('new_password2')[0], "The two password fields didn’t match.")

    def test_change_password_without(self):
        """
        Test the change password without data
        """

        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        data_p = {}
        # login
        response = self.client.post(self.url_login, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))
        # change password
        res_change = self.client.post(self.url_change_password, data=data_p)
        self.assertEquals(res_change.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(res_change.json().get('new_password1')[0], "This field is required.")
        self.assertEquals(res_change.json().get('new_password2')[0], "This field is required.")


    def test_get_user_information(self):
        """
        Test the get the user information
        """

        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        # login
        response = self.client.post(self.url_login, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))
        # get user information
        res_user = self.client.get(self.url_get_user)
        self.assertEquals(res_user.status_code, status.HTTP_200_OK)
        self.assertEquals(res_user.data.get('first_name'), "juan")
        self.assertEquals(res_user.data.get('last_name'), "carlos")


    def test_change_user_information(self):
        """
        Test the change of the user information
        """

        data = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        data_user = {
            'first_name': 'roberto',
            'last_name': 'pirada'
        }
        # login
        response = self.client.post(self.url_login, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('key'))
        # change information
        res_user = self.client.put(self.url_get_user, data=data_user)
        self.assertEquals(res_user.status_code, status.HTTP_200_OK)
        self.assertEquals(res_user.data.get('first_name'), "roberto")
        self.assertEquals(res_user.data.get('last_name'), "pirada")

