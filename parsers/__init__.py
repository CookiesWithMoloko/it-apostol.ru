import sqlalchemy.sql.compiler
from flask_sqlalchemy import SQLAlchemy
from models import People, StudyDirection, University
from time import time
from threading import Thread
import re
from app import app
class ParserStatus:
    def __init__(self, display: str, status: bool, color: str):
        self._display = display
        self._status = status
        self._color = color
    def get_color(self):
        return self._color
    def get_text(self):
        return self._display
    def get_status(self):
        return self._status
    def __bool__(self):
        return self._status
    def __str__(self):
        return self._display
class StatusList:
    ACTIVE = ParserStatus('Активно', True, '#026800')
    DISABLED = ParserStatus('Отключено', False, '#D31414')
    ON_UPDATE = ParserStatus('На обновлении', False, '#FFC803')

class ParserBase:
    def __init__(self,
                 database: SQLAlchemy,
                 interval: int,
                 last_use: int = 0):
        self.db: SQLAlchemy = database
        self.status: ParserStatus = StatusList.ACTIVE
        self.last_use = last_use
        self.interval = interval
        self.id = -1
        self._number_pattern = re.compile('^[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}$')
        self.active = True
        self.model = None
    def as_dict(self):
        return {
            'name': self.name,
            'status': str(self.status),
            'id': self.id,
            'last_use': self.last_use,
            'dirs': [
                i.name for i in self.dirs
            ]
        }
    def is_actual(self):
        return not self.status or (self.last_use + self.interval >= time())

    def exec(self) -> None:
        self.last_use = time()
    def get_model(self) -> University:
        if self.model is None:
            self.model = University.query.filter_by(id=self.id).first().as_dict()
        return self.model
    def add_people(self,
                   study_id: int,
                   link: str,
                   agreed: bool = False,
                   reg_number: int = None,
                   ins_number: str = None,
                   name: str = None) -> int:
        """return People().id"""

        p = People.query.filter(
            (
                    (People.name == name) & (People.name != None) |
                    (People.ins_number == ins_number) & (People.ins_number != None) |
                    (People.reg_number == reg_number) & (People.reg_number != None)
            ) &
            (People.study_id == study_id) &
            (People.university_id == self.id)
        ).first()
        if p is None:
            return self._add_people(reg_number=reg_number, ins_number=ins_number, name=name, study_id=study_id,
                                    link=link, agreed=agreed)
        else:
            self._update_people(id=p.id, reg_number=reg_number, ins_number=ins_number,
                                name=name, study_id=study_id, link=link, agreed=agreed
                                )
            return p.id

    def _add_people(self,
                    study_id: int,
                    link: str,
                    agreed: bool = False,
                    reg_number: int = None,
                    ins_number: str = None,
                    name: str = None) -> int:
        if len(list(filter(lambda a: a is not None, [reg_number, ins_number, name]))) == 0:
            return
        obj = People(
            reg_number=reg_number,
            ins_number=ins_number,
            name=name,
            study_id=study_id,
            link=link,
            agreed=agreed,
            add=int(time()),
            change=int(time()),
            university_id=self.id
        )
        self.db.session.add(obj)
        self.db.session.commit()
        return obj.id

    def _update_people(self,
                       id: int,
                       **kwargs) -> None:
        p: People = People.query.filter_by(id=id).first()
        st = False
        for key in kwargs.keys():
            if hasattr(p, key):
                if getattr(p, key) != kwargs[key]:
                    setattr(p, key, kwargs[key])
                    st = True
        if st:
            p.change = time()
            self.db.session.commit()

    @staticmethod
    def get_direction_id(name: str) -> int:
        s = StudyDirection.query.filter_by(name=name).first()
        if s is None:
            return -1
        return s.id
    @staticmethod
    def get_university_id(name: str) -> int:
        s = University.query.filter_by(name=name).first()
        if s is None:
            return -1
        return s.id
    def validate_number(self, number: str) -> bool:
        return not self._number_pattern.match(str(number)) is None


class ParserManager:
    def __init__(self):
        self.active = False
        self.parsers = []
        self.work = False
        self.t = None
        self.status = None

    @staticmethod
    def register(interval: int = 600,
                 author: str = '',
                 name: str = '',
                 link: str = '',
                 dirs: list = [],
                 id: int = -1):
        def r(f: ParserBase):
            if not issubclass(f, ParserBase):
                raise ValueError("ParserManager.register() work only on *(ParserBase)")

            def wrapper(*args, **kwargs):
                obj: ParserBase = f(*args, **kwargs, interval=interval)
                obj.__doc__ = f"SfeduAbitParser\nName: {name}\nAuthor: {author}\nLink: {link}\nUsage interval: {interval} seconds"
                obj.id = id
                dirs.sort()
                obj.dirs = list([StudyDirection.query.filter_by(name=i).first().as_dict() for i in dirs])
                obj.name = name
                return obj

            return wrapper

        return r

    def run(self, f: ParserBase) -> None:
        self.parsers.append(f)

    def post_register(self, *args, **kwargs) -> int:
        self.parsers = [
            i(*args, **kwargs) for i in self.parsers
        ]
        self.active = True
        return len(self.parsers)

    def exec(self) -> None:
        self.work = True
        if not self.active:
            raise RuntimeError("ParserManager.post_register() require for work ParserManager.exec()")
        for i in self.parsers:
            try:
                if not i.is_actual():
                    self.status = f'update {i}'
                    i.exec()
                    self.status = f'end update {i}'
            except Exception as e:
                print(e)
        self.work = False
        self.t = None

    def start_thread(self):
        self.exec()


manager = ParserManager()

