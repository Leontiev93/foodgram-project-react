from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class HexValidator(validators.RegexValidator):
    regex = r"^#([0-9a-fA-F]{3}){1,2}$"
    message = _(
        "Начало должна быть с # далее любое"
        "целое число от 0 до 9 и любая буква от A до F."
    )
    flags = 0


@deconstructible
class SlugValidator(validators.RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = _(
        "Введите любые буквы на литинице и целые числа, "
        "целое число от 0 до 9 и любая буква от A,a до Z,z."
    )
    flags = 0
