# Generated by Django 4.2.1 on 2023-05-20 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_alter_favorited_recipes_alter_favorited_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorited',
            name='recipes',
            field=models.ForeignKey(help_text='добавьте рецепт в избранном', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorited',
            name='user',
            field=models.ForeignKey(help_text='Кто добавляет рецепт в избранное', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]