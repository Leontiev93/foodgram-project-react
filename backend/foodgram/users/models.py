from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.core.validators import RegexValidator

from users.validators import FirstLastnameValidator


class User(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.LENGTH_USER,
        unique=True,
        validators=(UnicodeUsernameValidator(),
                    RegexValidator(
                        regex=r'\b(ME|me|Me|mE)\b',
                        message='Нельзя использовать имя me,Me,mE,ME',
                        code='invalid',
                        inverse_match=True,
        )),
        help_text=(
            'Требуется. Не более 150 символов. Только буквы, цифры и @/./+/-/_'
        ),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.LENGTH_USER,
        validators=(FirstLastnameValidator(),),
        help_text=('Введите свое имя'),
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LENGTH_USER,
        validators=(FirstLastnameValidator(),),
        help_text=('Введите свою фамилию'),
    )
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=settings.LENGTH_USER_EMAIL,
        unique=True,
        help_text=(
            'Введите электронный адрес в формате name@yandex.ru'
        ),
    )
    password = models.CharField(
        max_length=settings.LENGTH_USER,
        verbose_name='Пароль',
        help_text='Придумайте пароль'
    )
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('username', 'email')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_follower',
        verbose_name='Подписчик',
        help_text='Тот кто подписался',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_following',
        verbose_name='Кумир',
        help_text='Тот на кого подписались',
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=(
                'user', 'author'), name='unique_follow'),
            models.CheckConstraint(check=~models.Q(user=models.F(
                'author')), name='dont_follow_your_self'),
        ]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
