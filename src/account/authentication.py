from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailAuthBackend(object):
    """
    Authenticate users using email address
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return User.objects.get(email=username).order_by('id').first()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
