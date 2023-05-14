from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import validate_username_not_me


class User(AbstractUser):
    """Модель пользователя"""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = (
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username_not_me,
                    UnicodeUsernameValidator()
                    ),
        help_text=(
            'Требуется. Не более 150 символов. Только буквы, цифры и @/./+/-/_'
        ),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        help_text=(
            'Введите свое имя'
        ),
        )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text=(
            'Введите свою фамилию'
        ),
        )
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=254,
        help_text=(
            'Введите электронный адрес в формате name@yandex.ru'
        ),
        )
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        default=USER,
        verbose_name="Роль пользователя",
    )

    @property
    def is_admin(self):
        """Признак админа."""
        return (
            self.role == self.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        """Признак модератора."""
        return (
            self.role == self.MODERATOR
            or self.is_staff
        )
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        ordering = ('username', 'email')
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name="unique_fields"
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
