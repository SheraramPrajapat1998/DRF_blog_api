from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
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

