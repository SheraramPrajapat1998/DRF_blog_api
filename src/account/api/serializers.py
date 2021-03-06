from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from account.models import Referral

User = get_user_model()  # returns active User model


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = {
            'username': self.user.username,
            'id': self.user.id,
            'email': self.user.email,
            'success': True,
            'message': 'Successfully logged in!'
        }
        data.update(user_data)
        return data


class UserPublicSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="user-detail", lookup_field='pk')
    gender_description = serializers.CharField(
        source='get_gender_display', read_only=True)
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
    url = serializers.HyperlinkedIdentityField(
        view_name="user-detail", lookup_field='pk')
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source='get_gender_display', read_only=True)
    days_since_joined = serializers.IntegerField(
        source='get_days_since_joined', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            'url', 'id', 'username', 'first_name', 'last_name', 'full_name',
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


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password', 'password2', 'gender',
            'referral_code'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', "")
        referral_code = validated_data.pop('referral_code', '')

        if not password or not password2:
            raise serializers.ValidationError(
                {'message': "Password field can't be empty"})
        if (password != password2):
            raise serializers.ValidationError(
                {'message': "Passwords don't match"})
        instance = self.Meta.model(**validated_data)
        if password == password2 and password is not None:
            instance.set_password(password)
        instance.save()

        if referral_code:
            try:
                user = get_object_or_404(User, code=referral_code)
            except Exception as e:
                user = None
            if user:
                ref = Referral.objects.create(
                    referred_by=user, referred_to=instance)

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=2)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=2)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True, min_length=3, max_length=68)
    password2 = serializers.CharField(
        write_only=True, min_length=3, max_length=68)
    token = serializers.CharField(write_only=True, min_length=1)
    uidb64 = serializers.CharField(write_only=True, min_length=1)
