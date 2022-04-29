from app import app, db

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
