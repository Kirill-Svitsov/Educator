# Generated by Django 4.2.4 on 2023-08-10 14:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
