from app import app
from flask import render_template, request, make_response, redirect, url_for
from perms.auth import AuthUser


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('.index')))
    resp.delete_cookie('token')
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if AuthUser.get_user().is_authorized():
        return redirect(url_for('.index'))
    if request.method == 'GET':
        return render_template('login.html', show_login=False)
    elif request.method == 'POST':
        email = request.values.get('email', None)
        pwd = request.values.get('password', None)
        if email is None or pwd is None:
            return 'invalid args', 400
        from perms.exc import EmailNotFoundException, InvalidPasswordException
        try:
            token = AuthUser.auth_user(email, pwd)
        except EmailNotFoundException:
            return 'Email not found', 403
        except InvalidPasswordException:
            return 'Invalid password', 403
        resp = make_response(redirect(url_for('.index')))
        resp.set_cookie('token', token, 1_209_600)
        return resp
