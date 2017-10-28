import datetime

from peewee import *

from app import db


class Point(db.Model):
    longitude = TextField()  # 经度
    latitude = TextField()  # 维度
    treasure = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    # some_things = TextField()


class Tag(db.Model):
    tag = CharField()


class PointTag(db.Model):
    point = ForeignKeyField(Point)
    tag = ForeignKeyField(Tag)


def create_tables():
    Point.create_table()
    Tag.create_table()
    PointTag.create_table()
