from app import app, db
import flask
from perms.auth import AuthUser
flask._render_template = flask.render_template
def __rtp(*args, **kwargs):
    kw = dict(
        user=AuthUser.get_user(),
        show_login=True
    )
    for k, v in kwargs.items():
        kw[k] = v
    return flask._render_template(*args, **kw)

flask.render_template = __rtp

from parsers import manager as pm
import models

db.create_all()

import db_init
# Parsers
__import__('import_helper').import_dir('parsers', log=True)

# Routes
import routes


pm.post_register(database=db)
pm.start_thread()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
