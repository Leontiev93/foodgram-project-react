from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from tags.models import Tags
from users.models import User
from users.validators import FirstLastnameValidator


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=settings.LENGTH_RECIPES,
        validators=(FirstLastnameValidator(),)
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.LENGTH_RECIPES,
    )

    def __str__(self) -> str:
        return f'{self.name} измеряется в {self.measurement_unit}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=(
                'name', 'measurement_unit'), name='unique_ingredient'),
        ]
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
        max_length=settings.LENGTH_RECIPES,
        verbose_name='Название',
        help_text='добавьте название блюда',
    )
    tags = models.ManyToManyField(
        Tags,
        null=True,
        verbose_name='тег рецепта',
        help_text='добавьте тег рецепта',
    )
    image = models.ImageField(upload_to='media/photos/%Y%M%d/')
    text = models.TextField(
        verbose_name='описание',
        help_text='введите описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
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
        related_name='ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        help_text='Введите количество минимальное значение 1',
        default=1,
        validators=[
            MinValueValidator(1, 'минимальное значение 1')
        ]
    )

    def __str__(self) -> str:
        return f'В {self.recipes} -->{self.amount} {self.ingredient}'

    class Meta:
        verbose_name = 'Ингридиенты к рецептам'
        verbose_name_plural = 'Ингридиенты к рецептам'


class Favorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Пользователь',
        help_text='Кто добавляет рецепт в избранное',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Рецепт',
        help_text='добавьте рецепт в избранном',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=(
                'user', 'recipes'), name='unique_favorited'),
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Пользователь',
        help_text='Кто добавляет рецепт в корзину',
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Рецепт',
        help_text='добавлен рецепт в корзину',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=(
                'user', 'recipes'), name='unique_shoppingcart'),
        ]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
