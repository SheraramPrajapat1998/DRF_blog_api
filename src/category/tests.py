from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import Token
from account.api import views as account_api_views
from rest_framework import status
from account.tests import AccountUserTests
from category.api import views as category_api_views
from category.models import Category


User = get_user_model()


class CategoryTests(APITestCase):
    model = Category

    # category 1 data
    category1_name = 'Category1'
    category1_parent = None
    category1_is_active = True

    def get_user(self, username, email=None):
        return User.objects.get('username')

    def get_user_token(self, username, password):
        url = reverse(account_api_views.MyTokenObtainPairView.name)
        data = {
            "username": username,
            "password": password
        }
        resp = self.client.post(url, data=data, format='json')
        return resp.data

    def create_staffuser_and_set_token_credentials(self):
        account_instance = AccountUserTests()
        staff_user = account_instance.create_staff_user()
        self.set_user_token_credentials(
            staff_user.username, account_instance.staffuser1_password)

    def set_user_token_credentials(self, username, password):
        resp = self.get_user_token(username, password)
        # {
        #   'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MDAwMjcxOSwiaWF0IjoxNjQ5OTE2MzE5LCJqdGkiOiI0NTk2MDQzOWI4YWE0MjE1YmVhNzg4MTNlOTI4Yzg5YSIsInVzZXJfaWQiOjQsInVzZXJuYW1lIjoic3RhZmZ1c2VyMSIsImlkIjo0fQ.b6ZzUzLGV3mUVvUXk1WS-n89wbUzdEioPte0qkICQPM',
        #   'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5OTE2NjE5LCJpYXQiOjE2NDk5MTYzMTksImp0aSI6IjUyYjMzOTc4NjM1NDQwZjE5ZDVkNzcyZTc3N2FjZDE2IiwidXNlcl9pZCI6NCwidXNlcm5hbWUiOiJzdGFmZnVzZXIxIiwiaWQiOjR9.r3iPkwGbIalkyv-yhfEA0VWJ4yIEr9_yg93ODoNI7_E',
        #   'username': 'staffuser1', 'id': 4, 'email': 'staffuser1@gmail.com',
        #   'success': True, 'message': 'Successfully logged in!'
        # }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {0}'.format(resp.get('access')))

    def create_default_category(self):
        """
        Create a category having default parameters as
        ```
            name = Category1
            parent = None
            is_active = True
        ```
        """
        return self.create_category(category_name=self.category1_name,
                                    parent=self.category1_parent,
                                    is_active=self.category1_is_active)

    def create_category(self, category_name, parent=None, is_active=True):
        url = reverse(category_api_views.CategoryListAPIView.name)
        data = {
            "name": category_name,
            "parent": parent,
            "is_active": is_active
        }
        resp = self.client.post(url, data=data, format='json')
        return resp

    def get_category_collection(self):
        url = reverse(category_api_views.CategoryListAPIView.name)
        resp = self.client.get(url, format='json')
        return resp

    def test_post_creategory(self):
        self.create_staffuser_and_set_token_credentials()
        resp = self.create_default_category()
        resp_data = resp.data
        category1 = self.model.objects.get(
            name=self.category1_name, is_active=self.category1_is_active)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data.get('name'), self.category1_name)
        self.assertEqual(resp_data.get('parent'), self.category1_parent)
        self.assertEqual(resp_data.get('is_active'), self.category1_is_active)
        self.assertEqual(self.model.objects.count(), 1)

    def test_get_category_collection(self):
        self.create_staffuser_and_set_token_credentials()
        self.create_category(self.category1_name,
                             self.category1_parent, self.category1_is_active)
        response = self.get_category_collection()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure we retrieve only one item
        # NOTE: pagination must be set for below results
        self.assertEqual(response.data['count'], 1)
        response_data_result0 = response.data['results'][0]
        self.assertEqual(
            response_data_result0['name'], self.category1_name)
        self.assertEqual(
            response_data_result0['is_active'], self.category1_is_active)
        self.assertEqual(
            response_data_result0['is_active'], self.category1_is_active)

    def test_post_existing_category(self):
        self.create_staffuser_and_set_token_credentials()
        resp1 = self.create_default_category()
        resp2 = self.create_default_category()
        self.assertEqual(resp1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_category_without_staffuser(self):
        resp = self.create_default_category()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_and_get_category(self):
        self.create_staffuser_and_set_token_credentials()
        resp = self.create_default_category()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), 1)
        cat_obj = self.model.objects.get()
        self.assertEqual(cat_obj.name, self.category1_name)
        self.assertEqual(cat_obj.is_active, self.category1_is_active)
        self.assertEqual(cat_obj.parent, self.category1_parent)

