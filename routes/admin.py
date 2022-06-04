import json

from app import app
from flask import abort, jsonify, render_template, request, Blueprint
from perms.auth import AuthUser
from parsers import manager

bp = Blueprint('admin', 'admin', url_prefix='/admin')

@bp.route('/')
@bp.route('/parsers')
@AuthUser.auth_required(
    permissions=['admin.parsers.view']
)
def index():
    return abort(401, description='Adminki nema')
    parsers = list([
        {
            "obj": i,
            "model": i.get_model()
        } for i in manager.parsers
    ])
    return render_template('admin/parsers.html', parsers=parsers)

app.register_blueprint(bp)

# @app.route('/user')
# def index_user():
#     user: AuthUser = AuthUser.get_user()
#     r = json.dumps(dict(
#             user=vars(user),
#             db_user=vars(user.user),
#             group=vars(user.perm.group)
#         ), default=lambda obj: f"<<non-serializable: {type(obj).__qualname__}>>")
#     if user.is_authorized():
#         return jsonify(json.loads(r))
#     return 'Not authorized'
#
