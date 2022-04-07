from rest_framework import serializers
from account.api.serializers import UserPublicSerializer

from blog.models import Post
from comment.api.serializers import CommentSerializer
from comment.models import Comment
from activity.api.serializers import ActivityDetailSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    status_description = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Post
        fields = (
            'url', 'id', 'title', 'author', 'content',
            'status', 'status_description', 'image',
            'created_at', 'updated_at', 'published_at',
            'category', 'total_comments',
            'total_activity', 'total_likes'
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    status_description = serializers.ReadOnlyField(source='get_status_display')
    comments = serializers.SerializerMethodField()
    activity = ActivityDetailSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'url', 'id', 'title', 'author', 'content',
            'status', 'status_description', 'image',
            'created_at', 'updated_at', 'published_at', 'category',
            'total_comments', 'comments',
            # 'get_all_activity',
            'total_activity',
            'activity',
            # 'total_likes', 'likes'
        )

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        request = self.context.get('request')
        comments_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(comments_qs, many=True, context={'request':request}).data
        return comments
