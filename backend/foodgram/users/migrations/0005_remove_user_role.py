# Generated by Django 4.2.1 on 2023-05-27 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_follow_created_user_following_alter_follow_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
