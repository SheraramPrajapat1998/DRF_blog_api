from category.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    category_level = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'category_level')