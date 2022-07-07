from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session
from models import People, StudyDirection, University
from time import time
from typing import List, Optional
import re
class ParserBase:
    def __init__(self):
        self.__session: Optional[Session] = None
        self.id = -1
        self._number_pattern = re.compile('^[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}$')
        self.active = True
        self.model = None
        self.name: str = 'ParserDefault'
        self.dirs: List[StudyDirection] = []
    def get_count_peoples(self) -> int:
        return People.query.filter_by(university_id=self.id).count()
    def as_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'dirs': [
                i['name'] for i in self.dirs
            ]
        }
    def is_actual(self):
        return False

    def exec(self) -> None:
        pass
    def after_exec(self) -> None:
        pass
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

        print(
            'add_people', ins_number, agreed
        )

    def _add_people(self,
                    study_id: int,
                    link: str,
                    agreed: bool = False,
                    reg_number: int = None,
                    ins_number: str = None,
                    name: str = None) -> int:
        if len(list(filter(lambda a: a is not None, [reg_number, ins_number, name]))) == 0:
            return -1
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
        self.__session.add(obj)
        self.__session.commit()
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
            self.__session.commit()

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
