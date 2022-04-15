from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import Token
from account.api import views as account_api_views
from rest_framework import status

User = get_user_model()


# Create your tests here.
class AccountUserTests(APITestCase):
    model = User

    # test user data
    testuser1_first_name = 'test1'
    testuser1_last_name = 'user1'
    testuser1_username = 'testuser1'
    testuser1_password = 'testabc@123'
    testuser1_email = 'testuser1@gmail.com'
    testuser1_gender = User.MALE

    # staff user data
    staffuser1_first_name = 'staff1'
    staffuser1_last_name = 'user1'
    staffuser1_username = 'staffuser1'
    staffuser1_password = 'staffabc@123'
    staffuser1_email = 'staffuser1@gmail.com'
    staffuser1_gender = User.MALE


    def get_user_token(self, username, password, client=None):
        url = reverse(account_api_views.MyTokenObtainPairView.name)
        data = {
            "username": username,
            "password": password
        }
        client = client or self.client
        resp = client.post(url, data=data, format='json')
        print(resp.access)
        return resp

    def set_user_token_credentials(self, username, password, client=None):
        resp = self.get_user_token(username, password, client)
        print('resp', resp, resp.access)


    def create_user_and_set_token_credentials(self):
        user = self.register_user()
        token = Token.objects.create(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {0}'.format(token.key))

    def create_staff_user(self):
        data = {
            "username": self.staffuser1_username,
            "first_name": self.staffuser1_first_name,
            "last_name": self.staffuser1_last_name,
            "email": self.staffuser1_email,
            "password": self.staffuser1_password,
            "gender": self.staffuser1_gender,
            "is_staff": True,
            "is_superuser": True
        }
        staff_user = User.objects.create_user(**data)
        return staff_user

    def register_default_testuser(self):
        """
        Register a user with default parameters like
        ```
            first_name  = test1
            last_name   = user1
            username    = testuser1
            password    = abc@123
            email       = testuser1@gmail.com
            gender      = M
        ```
        """
        return self.register_user(
            username=self.testuser1_username, email=self.testuser1_email, password=self.testuser1_password,
            password2=self.testuser1_password, gender=self.testuser1_gender,
            first_name=self.testuser1_first_name, last_name=self.testuser1_last_name
        )

    def register_user(self, username, email, password, password2, gender=None, first_name="", last_name=""):
        url = reverse(account_api_views.UserRegisterAPIView.name)
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password2': password2,
            'gender': gender,
            'first_name': first_name,
            'last_name': last_name
        }
        response = self.client.post(url, data=data, format='json')
        return response

    def test_register_user(self):
        response = self.register_user(
            username=self.testuser1_username, email=self.testuser1_email, password=self.testuser1_password,
            password2=self.testuser1_password, gender=self.testuser1_gender,
            first_name=self.testuser1_first_name, last_name=self.testuser1_last_name
        )
        user = self.model.objects.get(
            username=self.testuser1_username, email=self.testuser1_email)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] == True
        assert response.data['message'] == "Account created successfully!"
        assert user.check_password(self.testuser1_password)
        assert User.objects.count() == 1
        assert user.username == self.testuser1_username
        assert user.email == self.testuser1_email
        assert user.gender == self.testuser1_gender
        assert user.first_name == self.testuser1_first_name
        assert user.last_name == self.testuser1_last_name

    def test_create_existing_user(self):
        response1 = self.register_user(
            username=self.testuser1_username, email=self.testuser1_email, password=self.testuser1_password,
            password2=self.testuser1_password, gender=self.testuser1_gender,
            first_name=self.testuser1_first_name, last_name=self.testuser1_last_name
        )
        response2 = self.register_user(
            username=self.testuser1_username, email=self.testuser1_email, password=self.testuser1_password,
            password2=self.testuser1_password, gender=self.testuser1_gender,
            first_name=self.testuser1_first_name, last_name=self.testuser1_last_name
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user_collection(self):
        resp = self.register_default_testuser()
        url = reverse(account_api_views.UserListAPIView.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        # Make sure we retrieve only one item
        # NOTE: pagination must be set for below results
        assert response.data['count'] == 1
        response_data_result0 = response.data['results'][0]
        assert response_data_result0['email'] == self.testuser1_email
        assert response_data_result0['username'] == self.testuser1_username

