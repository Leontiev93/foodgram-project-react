from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from tags.validators import HexValidator

LENGTH = 200


class Tags(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=LENGTH,
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
        max_length=LENGTH,
        unique=True,
        verbose_name='адрес',
        help_text='введите уникальный слаг',
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
