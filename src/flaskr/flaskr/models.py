from flaskr import db
from peewee import *


class Entry(db.Model):
    title = CharField()
    text = CharField()


def init():
    Entry.create_table()
