from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
    name = 'token_obtain_pair'

class UserListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by('id')
    name = 'user-list'


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by('id')
    name = 'user-detail'


class UserRegisterAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserRegisterSerializer
    name = 'user_register'

    def get(self, request, format=None):
        serializer = self.serializer_class()
        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            email = request.data.get('email')
            subject = "Account Created !"
            message = f'Dear {new_user}, Your account has been created.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return Response(data={'success':True, 'message': 'Account created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    name = 'change-password'

    def get(self, request, format=None):
        serializer = self.serializer_class()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')
            print(old_password, new_password, confirm_password)
            if new_password != confirm_password:
                return Response(data={
                    'success':False,
                    'message':'new_password and confirm_password does not match.'
                }, status=status.HTTP_400_BAD_REQUEST)
            # check old password
            if not self.object.check_password(old_password):
                return Response(data={'success':True, 'old_password':['Wrong password']}, status=status.HTTP_400_BAD_REQUEST)
            # set password in hash/encripted form
            self.object.set_password(new_password)
            self.object.save()
            response = {
                'success':True,
                'message': 'Password set successfully!',
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
