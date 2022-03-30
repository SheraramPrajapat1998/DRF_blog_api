from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Category Name'),
        help_text=_('Required and Unique'), unique=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
        null=True, blank=False, related_name='children')
    is_active = models.BooleanField(default=True,
        help_text=_("A boolean field which shows whether the category is active or not"))
    category_level = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('name', )

    def get_category_level(self):
        return f'{self.category_level}'

    def get_category_data(self):
        if self.is_parent:
            return f'{self.name} (cat_level:{self.find_category_level()})'
        return f'{self.name} - {self.parent} (cat_level:{self.find_category_level()})'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.category_level = self.find_category_level()
        super().save(*args, **kwargs)

    def find_category_level(self):
        category_level = 1
        if self.parent is None:
            return category_level
        else:
            while self.parent is not None:
                self = self.parent
                category_level += 1
        return category_level

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
