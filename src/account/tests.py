from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

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

    def get_user_token(self, username, password):
        url = reverse(account_api_views.MyTokenObtainPairView.name)
        data = {
            'username': username,
            'password': password
        }
        resp = self.client.post(url, data=data, format='json')
        token = resp.get('access')
        return token

    def set_user_token_credentials(self, username, password):
        token = self.get_user_token(username, password)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))

    def create_default_testuser_and_set_token_credentials(self):
        user = self.register_default_testuser()
        token = Token.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token.key))

    def create_staff_user(self):
        data = {
            "username": self.staffuser1_username,
            "first_name": self.staffuser1_first_name,
            "last_name": self.staffuser1_last_name,
            "email": self.staffuser1_email,
            "password": self.staffuser1_password,
            "gender": self.staffuser1_gender
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
        user = self.model.objects.get(username=self.testuser1_username, email=self.testuser1_email)
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

    def test_get_user_token(self):
        self.create_staff_user()
        users = User.objects.all()
        print(users)
        print(self.get_user_token(self.testuser1_username, self.testuser1_password))

