from django.db import models
from django.conf import settings

from tags.validators import HexValidator
from users.validators import FirstLastnameValidator


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.LENGTH_TAGS,
        help_text='введите название тега',
        validators=(FirstLastnameValidator(),)
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=settings.LENGTH_TAGS_HEX,
        help_text='введите цвет тега (HEX)',
        validators=(HexValidator(),)
    )
    slug = models.SlugField(
        max_length=settings.LENGTH_TAGS,
        unique=True,
        verbose_name='адрес',
        help_text='введите уникальный слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.slug
