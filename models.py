from app import db


def as_dict(self):
    r = dict()
    def getr(name: str):
        if hasattr(self, name):
            r[name] = getattr(self, name).as_dict()
    for c in self.__table__.columns:
        a = getattr(self, c.name)
        if isinstance(a, db.Model):
            r[c.name] = a.as_dict()
        else:
            r[c.name] = a
    getr('university')
    getr('study')
    return r


db.Model.as_dict = as_dict


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    ins_number = db.Column(db.String(14), nullable=True)
    reg_number = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(128), nullable=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    study_id = db.Column(db.Integer, db.ForeignKey('studydirection.id'), nullable=False)
    link = db.Column(db.String(128), nullable=False)
    agreed = db.Column(db.Boolean, default=False)
    add = db.Column(db.BigInteger, nullable=False)
    change = db.Column(db.BigInteger, nullable=False)
    study = db.relationship("StudyDirection", backref="people", uselist=False)
    university = db.relationship("University", backref="people", uselist=False)


class University(db.Model):
    __tablename__ = 'university'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    link = db.Column(db.String(128), unique=True, nullable=False)


class StudyDirection(db.Model):
    __tablename__ = 'studydirection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)


class AuthClient(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    vk = db.Column(db.BigInteger, nullable=True)
    token = db.Column(db.String(128), unique=True, nullable=False)
    ip = db.Column(db.String(32), unique=False)
    reg_date = db.Column(db.BigInteger, nullable=False)
    auth_date = db.Column(db.BigInteger, nullable=False)
