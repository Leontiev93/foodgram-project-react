from django.db import models


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        help_text='введите название тега',
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=16,
        help_text='введите цвет тега (HEX)',
        blank=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='адрес',
        help_text='введите уникальный слаг',
        blank=True,
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
