import json

from app import app
from flask import abort, jsonify, render_template, request
from perms.auth import AuthUser

@app.route('/admin')
def admin():
    abort(401, description='Adminki nema')


@app.route('/test_search')
def test_search():
    if request.remote_addr != '93.178.115.79':
        return abort(401, description="пашол нахуй умный фронт")
    return render_template('test_search.html')
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
# @app.route('/get_admin')
# def get_admin():
#     user: AuthUser = AuthUser.get_user()
#     user.perm.add_permission('*')
#     return jsonify(list(user.perm.user.permissions))
#
# @app.route('/reg_admin')
# def reg_admin():
#     return str(AuthUser.register('admin@mail.ru', 'admin', display_name='Администратор TEST'))
