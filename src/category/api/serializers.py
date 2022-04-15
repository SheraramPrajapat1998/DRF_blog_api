from category.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', lookup_field='pk')
    category_level = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'parent', 'category_level', 'is_active')
