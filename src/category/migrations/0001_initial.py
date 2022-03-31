# Generated by Django 4.0.3 on 2022-03-30 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Required and Unique', max_length=50, unique=True, verbose_name='Category Name')),
                ('is_active', models.BooleanField(default=True, help_text='A boolean field which shows whether the category is active or not')),
                ('category_level', models.PositiveIntegerField()),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='category.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
    ]