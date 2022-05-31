from app import app

from flask import request, jsonify
import api.methods
from api import api


@app.route('/api/<method>', methods=['GET', 'POST'])
@app.route('/api')
def api_main(method: str = ''):
    return jsonify(api.execute(method, request.values).as_dict())
