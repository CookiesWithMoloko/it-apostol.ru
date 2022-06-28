import flask
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import dotenv
dotenv.load_dotenv()


app = Flask(__name__, static_folder='static')


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = f"""
    mysql+pymysql://
    {os.environ.get('DB_USER')}
    :{os.environ.get('DB_PASSWORD')}
    @{os.environ.get('DB_HOST')}
    /{os.environ.get('DB_NAME')}
""".translate(str.maketrans({'\n': '', '\r': '', ' ': ''}))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
DEBUG = True
if DEBUG:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    app.debug = True
app.url_map.strict_slashes = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)
