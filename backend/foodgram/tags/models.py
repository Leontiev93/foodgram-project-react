from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings

from tags.validators import HexValidator, SlugValidator


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.LENGTH_TAGS,
        help_text='введите название тега',
        validators=(UnicodeUsernameValidator(),
                    )
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=16,
        help_text='введите цвет тега (HEX)',
        validators=(HexValidator(),
                    )
    )
    slug = models.SlugField(
        max_length=settings.LENGTH_TAGS,
        unique=True,
        verbose_name='адрес',
        help_text='введите уникальный слаг',
        validators=(SlugValidator(),
                    )
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
