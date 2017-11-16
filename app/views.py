from flask import render_template, request, redirect, send_from_directory

from app import app
from models import Point, Tag, PointTag, LogPoint


@app.route('/')
def homepage():
    x = Point.select().order_by(Point.created_date.desc()).execute()
    return render_template('index.html', points=x)


@app.route('/filter.html')
def filter():
    tags = Tag.select().execute()
    return render_template('filter.html', tags=tags)


@app.route('/tag/<tag>')
def query_tag(tag):
    x = (Point.select().join(PointTag).join(Tag)
         .where(Tag.tag == tag)
         .order_by(Point.created_date.desc()))
    return render_template('index.html', points=x)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':

        return render_template('register.html')
    elif request.method == 'POST':
        """longitude:
latitude:
latitude:
projectpoi-captcha-token:iumX9JGxpsboLvAwuUmxcC00
Name
"""
    pass


@app.route('/post', methods=["POST"])
def post():
    longitude = request.form.get('longitude', '')
    latitude = request.form.get('latitude', '')
    treasure = request.form.getlist('treasure')
    if not (isfloat(latitude) and isfloat(longitude) and treasure):
        return redirect('/post.html')
    try:
        tags = [Tag.get(tag=x) for x in treasure]
    except Tag.DoesNotExist:
        return redirect('/post.html')

    x, obj_created = Point.get_or_create(latitude=latitude, longitude=longitude,
                                         defaults={'treasure': ', '.join(treasure)})  # type:Point,bool
    if obj_created:
        for y in tags:
            PointTag.create(tag=y, point=x)
        l = LogPoint.create(latitude=latitude,
                            longitude=longitude,
                            treasure=', '.join(treasure),
                            created_date=x.created_date)
    else:
        return '坐标已存在 <a href="/post.html">重新分享</a>'
    return redirect('/')


@app.route('/post.html')
def show_post():
    return render_template('post.html', tags=Tag.select().execute())
    # Point.get_or_create(latitude=latitude, longitude=longitude,
    #                     defaults={'treasure': ', '.join(treasure)})
    # return redirect('/')


@app.route('/log')
def log():
    x = (LogPoint.select()
         .order_by(LogPoint.created_date.desc()))
    return render_template('index.html', points=x)


@app.route('/nearest/<float:lon>/<float:lat>')
def near(lon, lat):
    x = list(Point.select().order_by(Point.created_date.desc()).execute())  # type: list[Point]
    x.sort(key=lambda x: (float(x.longitude) - lon) ** 2 + (float(x.latitude) - lat) ** 2)
    return render_template('index.html', points=x)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
