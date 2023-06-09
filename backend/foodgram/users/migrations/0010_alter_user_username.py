# Generated by Django 4.2.1 on 2023-06-19 08:51

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует'}, help_text='Требуется. Не более 150 символов. Только буквы, цифры и @/./+/-/_', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), django.core.validators.RegexValidator(code='invalid', inverse_match=True, message='Нельзя использовать имя me,Me,mE,ME', regex='(?:me|Me|mE|ME)')], verbose_name='Имя пользователя'),
        ),
    ]
