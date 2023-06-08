from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\z"
    message = _(
        "Введите любые буквы на литинице и целые числа, "
        "целое число от 0 до 9 и любая буква от A,a до Z,z."
        "а так же символы -, @"
    )
    flags = 0