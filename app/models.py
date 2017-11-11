import datetime

import pytz
from peewee import *

from app import db

tz = pytz.timezone('Asia/Shanghai')


class Point(db.Model):
    id = PrimaryKeyField()
    longitude = TextField()  # 经度
    latitude = TextField()  # 维度
    treasure = TextField()
    created_date = DateTimeField(default=lambda: datetime.datetime.now(tz))


class Tag(db.Model):
    id = PrimaryKeyField()
    tag = TextField()


class PointTag(db.Model):
    point = ForeignKeyField(Point, related_name='pointtag')
    tag = ForeignKeyField(Tag, related_name='pointtag')


class LogPoint(db.Model):
    longitude = TextField()  # 经度
    latitude = TextField()  # 维度
    treasure = TextField()
    created_date = TextField()


def create_tables():
    Point.create_table()
    Tag.create_table()
    PointTag.create_table()
    LogPoint.create_table()
