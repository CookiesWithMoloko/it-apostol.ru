from app import db
from models import University, StudyDirection

u = (
    University(name='sfedu', display_name='ЮФУ', link='https://sfedu.ru', description=''),
    University(name='vsuet', display_name='ВГУИТ', link='https://vsuet.ru', description='')
)
s = (
    StudyDirection(name='10.05.03', description='ИБАС'),
    StudyDirection(name='10.05.05', description=''),
    StudyDirection(name='10.05.02', description=''),
    StudyDirection(name='10.03.01', description='')
)
for i in u:
    if University.query.filter_by(name=i.name).first() is None:
        db.session.add(i)
for i in s:
    if StudyDirection.query.filter_by(name=i.name).first() is None:
        db.session.add(i)

