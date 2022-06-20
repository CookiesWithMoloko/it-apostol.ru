from api.argument import Argument
from typing import List
from werkzeug.datastructures import MultiDict
from api.answer import ApiAnswer
from api.validator import Validator
from perms.exc import *
from perms.auth import AuthUser
from typing import Callable

class ApiMethod:
    def __init__(self, *,
                 name: str,
                 action,
                 args: list,
                 ret: Validator,
                 permissions: List[str] = None,
                 authorization_required: bool = True
                 ):
        self.name = name
        self.ret = str(ret)
        self.args = args
        self.action = action
        self.length = len(list(filter(lambda a: a.default is not None, args)))
        self.permissions: List[str] = permissions if permissions is not None else list()
        self.authorization_required: bool = authorization_required or len(self.permissions) > 0
    def as_dict(self):
        i: Argument
        return {
            "name": self.name,
            "return": self.ret,
            "args": list([
                i.as_dict() for i in self.args
            ]),
            "auth_required": self.authorization_required
        }
    def __doc__(self, d=False):
        return f"{self.name} -> {self.ret}"

    def execute(self, args: MultiDict) -> ApiAnswer:
        if self.authorization_required:
            user = AuthUser.get_user()
            if not user.is_authorized():
                return ApiAnswer(False, error=AuthorizationRequiredException())
            for p in self.permissions:
                if not user.has_permission(p):
                    return ApiAnswer(False, error=PermissionDeniedException(p))
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
                 permissions: List[str] = None,
                 auth_required: bool = True,
                 args: list = [],
                 ) -> Callable[[], None]:
        def r(f):
            self.methods.append(
                ApiMethod(
                    name=name,
                    ret=ret,
                    args=args,
                    action=f,
                    authorization_required=auth_required,
                    permissions=permissions
                )
            )

        return r


api = Api()
