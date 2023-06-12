# Generated by Django 4.2.1 on 2023-06-12 07:54

import django.contrib.auth.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует'}, help_text='Требуется. Не более 150 символов. Только буквы, цифры и @/./+/-/_', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), users.validators.validate_username_not_me], verbose_name='Имя пользователя'),
        ),
    ]
