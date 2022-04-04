from rest_framework import views, generics
from rest_framework import permissions
from .import serializers
from category.models import Category
from core.api.permissions import IsStaffOrReadOnly


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = serializers.CategorySerializer
    name = 'category-list'
    permission_classes = (IsStaffOrReadOnly, )


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = serializers.CategorySerializer
    name = 'category-detail'
    permission_classes = (IsStaffOrReadOnly, )

