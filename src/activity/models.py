from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.

class ActivityManager(models.Manager):
    def get_content_type(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def filter_by_instance(self, instance, activity_type=None):
        content_type = self.get_content_type(instance)
        object_id = instance.id
        qs = super().filter(content_type=content_type, object_id=object_id)
        if activity_type is None:
            return qs
        if activity_type:
            qs = qs.filter(activity_type=activity_type)
        else:
            pass
        return qs


class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_activity')
    activity_type = models.CharField(choices=ACTIVITY_TYPES, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    objects = ActivityManager()

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.get_activity_type_display()}(id: {self.id} on '{self.content_object}'(id: {self.object_id}))"

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
