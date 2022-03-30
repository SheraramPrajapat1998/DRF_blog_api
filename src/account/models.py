from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_days_since_joined(self):
        return (timezone.now() - self.date_joined).days
