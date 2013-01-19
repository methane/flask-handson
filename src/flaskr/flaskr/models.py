from flaskr import db
from sqlalchemy import *


class Entry(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    text = Column(Text)


def init():
    db.create_all()
