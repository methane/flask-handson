from flask import Flask
from flask_peewee.db import Database

app = Flask(__name__)
app.config.update(
        DATABASE={
            'name': 'flaskr.db',
            'engine': 'peewee.SqliteDatabase',
            },
        SECRET_KEY="secret key",
        )

db = Database(app)

import flaskr.views
