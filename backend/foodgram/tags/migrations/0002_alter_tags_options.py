# Generated by Django 4.2.1 on 2023-05-16 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tags',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]