from app import app
from flask import abort, jsonify
from perms.auth import AuthUser

@app.route('/admin')
def admin():
    abort(401, description='Adminki nema')

@app.route('/user')
def index_user():
    user: AuthUser = AuthUser.get_user()
    if user.is_authorized():
        return jsonify(user.user.as_dict())
    return 'Not authorized'
