from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utils import generate_unique_user_code

class Referral(models.Model):
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='referrals', null=True, blank=True)
    referred_to = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_query_name='has_referred', null=True, blank=True)


class User(AbstractUser, PermissionsMixin):
    MALE = "M"
    FEMALE = "F"
    OTHERS = "O"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHERS, "Others"),
    )
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=2)
    email = models.EmailField(_('Email Address'), blank=False, null=False)
    code = models.CharField(_('Code'), unique=True, null=False, max_length=10, default=generate_unique_user_code)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_days_since_joined(self):
        return (timezone.now() - self.date_joined).days

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_user_code()
        return super().save(*args, **kwargs)

