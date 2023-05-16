from django.db import models
from django.core.validators import MinValueValidator

from ingredients.models import Ingredient
from tags.models import Tags
from users.models import User


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор рецепта',
        help_text='Автор рецепта',
    )
    tags = models.ManyToManyField(
        Tags,
        null=True,
        related_name='recipes',
        verbose_name='тег рецепта',
        help_text='добавьте тег рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsToRecipes'
    )
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/photos/%Y%M%d/')
    text = models.TextField(
        verbose_name='описание',
        help_text='введите описание',
    )
    cooking_time = models.IntegerField(
        verbose_name='время приготовления в минутах ',
        help_text='введите время приготовления в минутах',
        validators=[
            MinValueValidator(1, 'минимальное значение 1')
            ]
        )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientsToRecipes(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='количество',
        help_text='Введите количество минимальное значение 1',
        validators=[
            MinValueValidator(1, 'минимальное значение 1')
            ]
        )

    def __str__(self) -> str:
        return f'{self.ingredient} в {self.recipes}'

    class Meta:
        verbose_name = 'Ингридиенты к рецептам'
        verbose_name_plural = 'Ингридиенты'
