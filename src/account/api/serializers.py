from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model() #returns active User model

class UserPublicSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail", lookup_field='pk')
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = (
            'url', 'id', 'username', 'gender',
            'gender_description', 'full_name',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', )


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)
    days_since_joined = serializers.IntegerField(source='get_days_since_joined', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'email', 'gender', 'gender_description', 'days_since_joined',
            'is_active',  'date_joined', 'last_login'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation['is_superuser'] = True
        else:
            representation['is_superuser'] = False
        if instance.is_staff:
            representation['is_staff'] = True
        else:
            representation['is_staff'] = False
        return representation
