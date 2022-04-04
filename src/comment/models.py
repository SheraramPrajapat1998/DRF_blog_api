from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class CommentManager(models.Manager):
    def all(self):
        qs = super().filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        qs = super().filter(content_type=content_type, object_id=object_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        if self.is_parent:
            return f"comment {self.id} by {self.user}"
        return f"reply {self.id} to comment {self.parent.id} by {self.user}"

    def children(self):
        return Comment.objects.select_related('user').filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def total_replies(self):
        return self.children().count()
