from rest_framework import serializers
from django.contrib.auth import authenticate

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


def validate_email_password(self, attrs):
    """Валидатор, проверяет соответствие почты и пароля."""
    email = attrs.get('email')
    password = attrs.get('password')

    if email and password:
        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)
        if not user:
            msg = _('Не возможно войти в систему email и password не совпадают.')
            raise serializers.ValidationError(msg, code='authorization')
    else:
        msg = _('Must include "email" and "password".')
        raise serializers.ValidationError(msg, code='authorization')

    attrs['user'] = user
    return attrs
