from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FirstLastnameValidator(validators.RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z\-]+$'
    message = _(
        "Введите любые буквы на литинице/кирилице"
    )
    flags = 0
