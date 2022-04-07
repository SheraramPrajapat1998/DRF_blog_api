from django.utils import timezone
from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _
from activity.models import Activity
from category.models import Category
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

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
    activity = GenericRelation(Activity)

    class Meta:
        ordering = ('-published_at', 'title', '-created_at')

    def __str__(self):
        return self.title

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def total_comments(self):
        return self.comments.count()

    # @property
    # def get_all_activity(self):
    #     qs = Activity.objects.select_related('user').filter_by_instance(instance=self)
    #     return qs

    # @property
    # def get_likes(self):
    #     qs = self.get_all_activity.filter(activity_type=Activity.LIKE)
    #     return qs

    # @property
    # def total_likes(self):
    #     num_likes = self.get_likes.count()
    #     return num_likes

    @property
    def activity_filter(self, qs, activity_type=None):
        return qs.filter(activity_type=activity_type) 

    @property
    def get_all_activity(self):
        activities = self.activity.all()
        return activities

    @property
    def get_all_likes(self):
        likes = self.get_all_activity.filter(activity_type=Activity.LIKE)
        return likes

    @property
    def total_likes(self):
        return self.get_all_likes.count()

    @property
    def total_activity(self):
        return self.get_all_activity.count()
