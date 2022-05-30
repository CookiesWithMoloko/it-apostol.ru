from app import db
from models import University, StudyDirection, User
from perms.auth import AuthUser
u = (
    University(
        name='sfedu',
        display_name='ЮФУ',
        link='https://sfedu.ru',
        description='ЮЖНЫЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ'
    ),
    University(
        name='vsuet',
        display_name='ВГУИТ',
        link='https://vsuet.ru',
        description='ВОРОНЕЖСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ ИНЖЕНЕРНЫХ ТЕХНОЛОГИЙ'
    )
)
s = (
    StudyDirection(
        name='10.05.03',
        description='Информационная безопасность автоматизированных систем'
    ),
    StudyDirection(
        name='10.05.05',
        description='Безопасность информационных технологий в правоохранительной сфере'),
    StudyDirection(
        name='10.05.02',
        description='Информационная безопасность телекоммуникационных систем'
    ),
    StudyDirection(
        name='10.03.01',
        description='Информационная безопасность'
    )
)
for i in u:
    if University.query.filter_by(name=i.name).first() is None:
        db.session.add(i)
for i in s:
    if StudyDirection.query.filter_by(name=i.name).first() is None:
        db.session.add(i)
