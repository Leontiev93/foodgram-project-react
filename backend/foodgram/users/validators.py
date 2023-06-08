from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z\-\@]+$'
    message = _(
        "Введите любые буквы на литинице/кирилице и целые числа, "
        "целое число от 0 до 9, а так же символы -, @"
    )
    flags = 0
