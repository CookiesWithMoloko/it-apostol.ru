from api.validator import Validator
from api.answer import ApiAnswer

from perms.exc import *


class Argument:
    def __init__(self, name, form: Validator, default=None):
        self.name = name
        self.form = form
        self.value = None
        self.default = default

    class DEFAULT_NONE_CLASS:
        def __str__(self):
            return "None"

    NONE = DEFAULT_NONE_CLASS()

    def as_dict(self):
        return {
            "name": self.name,
            "required": self.default is None,
            "default": str(self.default),
            "type": self.form.name
        }

    @staticmethod
    def is_empty(value):
        return value is None or value == ''

    def get(self, value) -> ApiAnswer:
        t = self.form.check(value)
        if t is None and self.default is None:
            return ApiAnswer(False, error=InvalidArgumentException(self.name))
        elif t is None:
            return ApiAnswer(True, data=None if self.default is Argument.NONE else self.default)
        elif t is False:
            return ApiAnswer(False, error=InvalidArgumentTypeException(self.name, self.form))
        elif t:
            return ApiAnswer(True, data=value)

    def __str__(self):
        return f'{self.form.name}("{self.value}")'
