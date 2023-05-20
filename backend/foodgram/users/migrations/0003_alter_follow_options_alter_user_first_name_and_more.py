# Generated by Django 4.2.1 on 2023-05-20 20:58

import django.contrib.auth.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_follow_follow_unique_follow_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписки', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Введите свое имя', max_length=150, validators=[users.validators.validate_username_not_me, django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Введите свою фамилию', max_length=150, validators=[users.validators.validate_username_not_me, django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Фамилия'),
        ),
    ]
