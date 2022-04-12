from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import Referral
from . import serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from core.api.permissions import IsStaffOrUserOrReadOnly, IsUserOrReadOnly


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
    name = 'token_obtain_pair'

class UserListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by('id')
    name = 'user-list'


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by('id')
    name = 'user-detail'
    permission_clases = (IsStaffOrUserOrReadOnly, )


class UserRegisterAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserRegisterSerializer
    name = 'user_register'

    def get(self, request, format=None):
        serializer = self.serializer_class()
        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            email = request.data.get('email')
            subject = "Account Created !"
            message = f'Dear {new_user}, Your account has been created.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return Response(data={'success':True, 'message': 'Account created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    name = 'change-password'

    def get(self, request, format=None):
        serializer = self.serializer_class()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')
            if new_password != confirm_password:
                return Response(data={
                    'success':False,
                    'message':'new_password and confirm_password does not match.'
                }, status=status.HTTP_400_BAD_REQUEST)
            # check old password
            if not self.object.check_password(old_password):
                return Response(data={'success':True, 'old_password':['Wrong password']}, status=status.HTTP_400_BAD_REQUEST)
            # set password in hash/encripted form
            self.object.set_password(new_password)
            self.object.save()
            response = {
                'success':True,
                'message': 'Password set successfully!',
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = serializers.RequestPasswordResetSerializer
    name = 'request-reset-email'

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')
        if serializer.is_valid(raise_exception=True):
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                # for some reason smart_bytes is not adding extra padding
                # .i.e. urlsafe_base64_encode returns encoded string in mutiple of 4
                # and adds extra padding('=') to make it multiple of 4 if it isn't.
                extra_padding = "="*(len(uidb64)%4)

                uidb64 = uidb64 if len(uidb64) % 4 == 0 else f"{uidb64}{extra_padding}"
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request).domain
                relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token':token})
                abs_url = f"http://{current_site}{relative_link}"
                email_body = f"""Hi {user.username},
Use link below to reset your password.
{abs_url}
                """
                subject = "reset your password"
                send_mail(subject=subject, message=email_body, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
                return Response(data={'success': True, 'message': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPIView(generics.GenericAPIView):
    name = 'password-reset-confirm'

    def get(self, request, uidb64, token, format=None):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(data={'success': False, 'message': 'Token is invalid. Please request a new one.'})
            return Response(data={'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token})
        except DjangoUnicodeDecodeError as err:
            return Response(data={'success': False, 'message':'Token is invalid. Please request a new one.'})


class SetNewPasswordAPIView(generics.GenericAPIView):
    name = 'password-reset-complete'
    serializer_class = serializers.SetNewPasswordSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            password2 = request.data.get('password2')
            token = request.data.get('token')
            uidb64 = request.data.get('uidb64')

            if password != password2:
                return Response(data={'success': False, 'messsage': "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                id = force_str(urlsafe_base64_decode(uidb64))
            except Exception as e:
                print('exception while setting new password', str(e))
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                user = None
                return Response(data={'success': False, 'message': "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(data={'success': False, 'message': 'The link is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(password)
            user.save()
            return Response(data={'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralUserAPIView(generics.GenericAPIView):
    name = 'user_referral'
    model = User
    ref_model = Referral

    def get(self, request, code, format=None):
        if request.user.is_anonymous:
            return Response(data={'message': "User not logged in.", 'success': False})
        if request.user.code == code:
            return Response(data={'message': "Can't refer to yourself", 'success': False})
        try:
            user = get_object_or_404(self.model, code=code)
        except self.model.DoesNotExist:
            user = None
            return Response(data={'success':False, 'message':"Invalid referral code"})
        code_applied = self.ref_model.objects.filter(referred_to=request.user.pk).exists()
        if code_applied:
            return Response(data={'success': False, 'message': "You have already used someone's referral code."})
        if user:
            ref = self.ref_model.objects.create(referred_to=request.user, referred_by=user)
            return Response(data={'success': True, 'message': 'Referral Added successfully!'})
