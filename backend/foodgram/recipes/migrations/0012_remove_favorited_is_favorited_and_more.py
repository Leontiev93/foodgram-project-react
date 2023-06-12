# Generated by Django 4.2.1 on 2023-06-12 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0011_alter_ingredient_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorited',
            name='is_favorited',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='is_in_shopping_cart',
        ),
        migrations.AlterField(
            model_name='favorited',
            name='recipes',
            field=models.ForeignKey(help_text='добавьте рецепт в избранном', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorited',
            name='user',
            field=models.ForeignKey(help_text='Кто добавляет рецепт в избранное', on_delete=django.db.models.deletion.CASCADE, related_name='favorited', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipes',
            field=models.ForeignKey(help_text='добавлен рецепт в корзину', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(help_text='Кто добавляет рецепт в корзину', on_delete=django.db.models.deletion.CASCADE, related_name='shoppingcart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]