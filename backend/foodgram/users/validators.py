from django.core import validators
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class FirstLastnameValidator(validators.RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z -]+$'
    message = _(
        "Введите любые буквы на литинице/кирилице"
    )
    flags = 0


def validate_username_not_me(value):
    """Валидатор, не допускающий создания пользователя с ником 'me'."""
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать \'me\' в качестве юзернейма'
        )
    return value
