from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import Token
from account.api import views as account_api_views
from rest_framework import status

User = get_user_model()


# Create your tests here.

user_first_name = 'test1'
user_last_name = 'user1'
username1 = 'testuser1'
userpassword1 = 'abc@123'
useremail1 = 'testuser1@gmail.com'
usergender = User.MALE

class AccountUserTests(APITestCase):
    model = User

    def create_user_and_set_token_credentials(self):
        user = self.register_user()
        token = Token.objects.create(user)
        print(user, token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token.key))

    def register_default_user(self):
        return self.register_user()

    def register_user(self, username=username1, email=useremail1, password=userpassword1, password2=userpassword1, gender=None, first_name="", last_name=""):
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
            username=username1, email=useremail1, password=userpassword1,
            password2=userpassword1, gender=usergender,
            first_name=user_first_name, last_name=user_last_name
        )
        user = self.model.objects.get(username=username1, email=useremail1)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] == True
        assert response.data['message'] == "Account created successfully!"
        assert user.check_password(userpassword1)
        assert User.objects.count() == 1
        assert user.username == username1
        assert user.email == useremail1
        assert user.gender == usergender
        assert user.first_name == user_first_name
        assert user.last_name == user_last_name

    def test_create_existing_user(self):
        response1 = self.register_user(
            username=username1, email=useremail1, password=userpassword1,
            password2=userpassword1, gender=usergender,
            first_name=user_first_name, last_name=user_last_name
        )
        response2 = self.register_user(
            username=username1, email=useremail1, password=userpassword1,
            password2=userpassword1, gender=usergender,
            first_name=user_first_name, last_name=user_last_name
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user_collection(self):
        resp = self.register_default_user()
        url = reverse(account_api_views.UserListAPIView.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        # Make sure we retrieve only one item
        # NOTE: pagination must be set for below results
        assert response.data['count'] == 1
        response_data_result0 = response.data['results'][0]
        assert response_data_result0['email'] == useremail1
        assert response_data_result0['username'] == username1

