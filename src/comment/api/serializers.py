from rest_framework import serializers

from comment.models import Comment
from account.api.serializers import UserPublicSerializer


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail', lookup_field='pk')
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'url', 'user', 'id', 'content_type',
            'object_id', 'parent', 'content',
            'total_replies', 'created_at', 'updated_at'
        )


class CommentChildSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail', lookup_field='pk')
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'url', 'user',  'id', 'content',
            'created_at', 'updated_at'
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail', lookup_field='pk')
    replies = serializers.SerializerMethodField()
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'url', 'user', 'id', 'content_type', 'object_id',
            'content', 'replies', 'total_replies',
            'created_at', 'updated_at'
        )

    def get_replies(self, obj):
        request = self.context.get('request')
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True, context={'request':request}).data
        return None

