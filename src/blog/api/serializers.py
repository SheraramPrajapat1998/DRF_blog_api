from rest_framework import serializers
from account.api.serializers import UserPublicSerializer

from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    status_description = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Post
        fields = (
            'url', 'id', 'title', 'author', 'content',
            'status', 'status_description', 'image',
            'created_at', 'updated_at', 'published_at',
            'category',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    status_description = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Post
        fields = (
            'url', 'id', 'title', 'author', 'content',
            'status', 'status_description', 'image',
            'created_at', 'updated_at', 'published_at', 'category',
        )
