from app import app
from flask import abort


@app.route('/admin')
def admin():
    abort(401, description='Adminki nema')
