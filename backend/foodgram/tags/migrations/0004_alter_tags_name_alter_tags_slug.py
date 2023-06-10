# Generated by Django 4.2.1 on 2023-06-08 10:01

import django.contrib.auth.validators
from django.db import migrations, models
import tags.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_alter_tags_color_alter_tags_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(help_text='введите название тега', max_length=200, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='slug',
            field=models.SlugField(help_text='введите уникальный слаг', max_length=200, unique=True, verbose_name='адрес'),
        ),
    ]
