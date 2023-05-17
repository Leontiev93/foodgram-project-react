from django.db import models
from django.core.validators import MinValueValidator

from tags.models import Tags
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    def __str__(self) -> str:
        return f'{self.name} измеряется в {self.measurement_unit}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Игридиенты'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор рецепта',
        help_text='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='добавьте название блюда',
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
        related_name='recipes',
        through='IngredientsToRecipes'
    )
    is_favorited = models.BooleanField(
        verbose_name='Избранное',
        help_text='добавить в избраное',
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Корзина',
        help_text='добавить в корзину покупок',
    )
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
        verbose_name_plural = 'Ингридиенты к рецептам'
