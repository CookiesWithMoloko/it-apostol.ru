from flask import request,  render_template, make_response, redirect, url_for
from app import app
from parsers import manager
from datetime import datetime
from perms.auth import AuthUser
from api import api
from api.answer import ApiAnswer
@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/university')
def university():
    parsers = list([
        {
            "obj": i,
            "model": i.get_model()
        } for i in manager.parsers
    ])
    return render_template('university.html', parsers=parsers)

@app.route('/check', methods=['POST', 'GET'])
def get_result():
    r: ApiAnswer = api.execute('check', request.args)
    req = {
        'fio': request.args.get('fio', ''),
        'ins_number': request.args.get('ins_number', '')
    }
    for i, v in enumerate(r.data):
        r.data[i]['change'] = datetime.utcfromtimestamp(int(r.data[i]['change']) + 3 * 3600).strftime('%H:%M %d.%m.%Y')
    if r.status and len(r.data) != 0:
        return render_template('result.html', result=r.data, request=req)
    else:
        return render_template('error/people_not_found.html', error=r.as_dict())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email', None)
        pwd = request.form.get('password', None)
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




@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')
