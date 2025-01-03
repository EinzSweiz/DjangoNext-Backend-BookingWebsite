# Generated by Django 5.1.4 on 2025-01-03 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='has_unread_messages',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='conversationmessage',
            name='read_by',
            field=models.ManyToManyField(blank=True, related_name='read_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
