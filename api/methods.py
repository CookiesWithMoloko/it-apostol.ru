from api import api
from api.argument import Argument
from api.validator import Validator
from api.answer import ApiAnswer
from models import People
from parsers import manager, ParserBase
from perms.exc import *

@api.register(
    name='check',
    ret=Validator.List(Validator.String('StudyDirectionReq')),
    args=[
        Argument('fio', Validator.String(), default=Argument.NONE),
        Argument('ins_number', Validator.InsNumber(), default=None)
    ],
    auth_required=True
)
def check(fio, ins_number):
    if Argument.is_empty(ins_number):
        return ApiAnswer(False, error=MissedArgumentException('ins_number'))
    r = People.query.filter(
        ((People.name == fio) & (People.name != None)) |
        ((People.ins_number == ins_number) & (People.ins_number != None))
    ).all()
    return ApiAnswer(True, data=[i.as_dict() for i in r])

@api.register(
    name='update.time',
    ret=Validator.Group(
            Validator.String('name'), Validator.String(),
            Validator.String('time'), Validator.Integer('UnixTime')
    ),
    args=[],
    permissions=['admin.parsers.info']
)
def update_time():
    i: ParserBase
    return ApiAnswer(True, data={
        'manager': {
            'work': manager.work,
            'thread': str(manager.t),
            'status': manager.status
        },
        'parsers': [
            {
                'name': i.name,
                'time': i.last_use
            } for i in manager.parsers
        ]
    })

@api.register(
    name='update.force',
    ret=Validator.String('None'),
    args=[],
    permissions=['admin.parsers.force_update']
)
def update_force():
    try:
        manager.start_thread()
    except RuntimeWarning as e:
        return ApiAnswer(False, error=TextException('Parser already active'))
    return ApiAnswer(True, data={
        'count': len(manager.parsers)
    })

@api.register(
    name='parsers.list',
    args=[],
    ret=Validator.List(Validator.String('Parser')),
    permissions=['admin.parsers.list']
)
def parsers_list():
    return ApiAnswer(True, data=[
        i.as_dict() for i in manager.parsers
    ])


