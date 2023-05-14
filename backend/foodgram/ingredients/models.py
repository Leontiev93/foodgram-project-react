from django.db import models


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
        verbose_name = 'Игридиент'
        verbose_name_plural = 'Игридиенты'
