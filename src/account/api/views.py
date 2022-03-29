from django.contrib.auth import get_user_model
from rest_framework import generics

from . import serializers

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserPublicSerializer
    queryset = User.objects.all().order_by('id')
    name = 'user-list'


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by('id')
    name = 'user-detail'
