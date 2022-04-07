from activity.models import Activity
from rest_framework import serializers

from account.api.serializers import UserPublicSerializer

class ActivitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='activity-detail', lookup_field='pk')
    user = UserPublicSerializer(read_only=True)
    activity_type_description = serializers.CharField(source='get_activity_type_display', read_only=True)

    class Meta:
        model = Activity
        fields = (
            'url', 'user', 'id', 'activity_type',
            'activity_type_description', 'created_at',
            'content_type', 'object_id',
            # 'content_object',
        )


class ActivityDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='activity-detail', lookup_field='pk')
    user = UserPublicSerializer(read_only=True)
    activity_type_description = serializers.CharField(source='get_activity_type_display', read_only=True)

    class Meta:
        model = Activity
        fields = (
            'url', 'user', 'id', 'activity_type',
            'activity_type_description', 'created_at',
            'content_type', 'object_id',
            # 'content_object',
        )
