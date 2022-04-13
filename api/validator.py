import re


def secure(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except:
            return None

    return wrapper


class Validator:
    @staticmethod
    def is_empty(value):
        return value is None or value == ''

    def __init__(self, check, name):
        self.name = name
        self.check = secure(check)

    def __str__(self):
        return self.name

    @staticmethod
    def String(name='String'):
        def v(value):
            if Validator.is_empty(value):
                return None
            return True

        return Validator(v, name)

    @staticmethod
    def Integer(name='Integer'):
        def r(a):
            if Validator.is_empty(a):
                return None
            try:
                int(a)
                return True
            except ValueError:
                return False

        return Validator(r, name)

    @staticmethod
    def RegexMatch(pattern: str, name='Regex'):
        pattern = re.compile(pattern)

        def v(value):
            if Validator.is_empty(value):
                return None
            return bool(pattern.match(str(value)))

        return Validator(v, name)

    @staticmethod
    def List(element):
        element: Validator

        def v(arg):
            for i in arg.split(','):
                if not element.check(i):
                    return False
            return True

        return Validator(v, f'List<{element}>')
    @staticmethod
    def Dictionary(key, value):
        return Validator(lambda a: True, f'Dictionary<{key}, {value}>')
    @staticmethod
    def Group(*args):
        name = 'Group<'
        for i in range(len(args) // 2):
            name += f'({args[i*2]}, {args[i*2+1]}),'
        if name[-1:] == ',':
            name = name[:-1] + '>'
        else:
            name += '>'
        return Validator(lambda a: True, name)
    @staticmethod
    def InsNumber():
        return Validator.RegexMatch('^[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}$', 'InsNumber')

    @staticmethod
    def RegNumber():
        return Validator.Integer('RegNumber')
