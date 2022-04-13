from api.argument import Argument

from werkzeug.datastructures import MultiDict
from api.answer import ApiAnswer
from api.validator import Validator
class ApiMethod:
    def __init__(self, *,
                 name: str,
                 action,
                 args: list,
                 ret: Validator
                 ):
        self.name = name
        self.ret = str(ret)
        self.args = args
        self.action = action
        self.length = len(list(filter(lambda a: a.default is not None, args)))
    def as_dict(self):
        i: Argument
        return {
            "name": self.name,
            "return": self.ret,
            "args": list([
                i.as_dict() for i in self.args
            ])
        }
    def __doc__(self, d=False):
        return f"{self.name} -> {self.ret}"

    def execute(self, args: MultiDict) -> ApiAnswer:
        r = dict()
        i: Argument
        for i in self.args:
            t: ApiAnswer = i.get(args.get(i.name, default=None))
            if t.status:
                r[i.name] = args.get(i.name, default=None)
            else:
                return ApiAnswer(False, error=t.error)
        if len(r.keys()) >= self.length:
            return self.action(**r)
        return ApiAnswer(False, error=self.__doc__(True))

    def __str__(self):
        return self.__doc__()


class Api:
    def __init__(self):
        self.methods: list = []

    def execute(self, name, args):
        for i in self.methods:
            if i.name == name:
                return i.execute(args)
        return ApiAnswer(False, data=[i.as_dict() for i in self.methods])

    def register(self, *,
                 name: str,
                 ret: str,
                 permission: str = '',
                 args: list = [],
                 ):
        def r(f):
            self.methods.append(
                ApiMethod(
                    name=name,
                    ret=ret,
                    args=args,
                    action=f
                )
            )

        return r


api = Api()
