from rest_framework import serializers

USERNAME_MAX_LEN_VALUE = 150


def validate_username(value):
    """Валидатор поля Usernae"""
    if len(value) > USERNAME_MAX_LEN_VALUE:
        raise serializers.ValidationError(
            f'Максимальная длина превышает {USERNAME_MAX_LEN_VALUE} символов!'
        )
    return value


def validate_username_not_me(value):
    """Валидатор, не допускающий создания пользователя с ником 'me'."""
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать \'me\' в качестве юзернейма'
        )
    return value
