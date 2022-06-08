from datetime import datetime

import flask
from flask import request, render_template, url_for, abort

from api import api
from api.answer import ApiAnswer
from app import app
from parsers import manager
from perms.auth import AuthUser
from perms.exc import *
@app.route('/search')
def search():
    user = AuthUser.get_user()
    if not user.perm.has_permission('main.search'):
        return flask.redirect(url_for('.login'))
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
    r: ApiAnswer = api.execute('check', request.form)
    req = {
        'fio': request.values.get('fio', ''),
        'ins_number': request.values.get('ins_number', '')
    }
    try:
        r.throw()
    except PermissionDeniedException as e:
        if not AuthUser.get_user().perm.has_permission('main.search'):
            return abort(401, description=str(e))
        return flask.redirect(url_for('.login'))
    for i, v in enumerate(r.data):
        r.data[i]['change'] = datetime.utcfromtimestamp(int(r.data[i]['change']) + 3 * 3600).strftime('%H:%M %d.%m.%Y')
    if r.status and len(r.data) != 0:
        return render_template('result.html', result=r.data, request=req)
    else:
        return render_template('error/people_not_found.html', show_login=False)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')
