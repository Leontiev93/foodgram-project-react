# Generated by Django 4.2.1 on 2023-06-17 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Придумайте пароль', max_length=150, verbose_name='Пароль'),
        ),
    ]
