from django.utils import timezone
from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _
from category.models import Category
from django.contrib.contenttypes.models import ContentType

# Create your models here.



class Post(models.Model):
    DRAFT = 'draft'
    PUBLISH = 'publish'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISH, 'Publish'),
    )

    title = models.CharField(verbose_name=_("Post Title"), max_length=50)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to='blog/posts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-published_at', 'title', '-created_at')

    def __str__(self):
        return self.title

