from flask import render_template, request, redirect

from app import app
from models import Point, Tag, PointTag


@app.route('/')
def homepage():
    x = Point.select().order_by(Point.created_date.desc()).execute()
    # print(x.__dict__)
    return render_template('index.html', points=x)


@app.route('/tag/<tag>')
def query_tag(tag):
    x = (Point.select().join(PointTag).join(Tag)
         .where(Tag.tag == tag)
         .order_by(Point.created_date.desc()))

    # x = Point.select().order_by(Point.created_date.desc()).execute()
    # print(x.__dict__)
    return render_template('index.html', points=x)


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
                                         defaults={'treasure': ', '.join(treasure)})
    if obj_created:
        for y in tags:
            PointTag.create(tag=y, point=x)
    return redirect('/')


@app.route('/post.html')
def show_post():
    return render_template('post.html', tags=Tag.select().execute())
    # Point.get_or_create(latitude=latitude, longitude=longitude,
    #                     defaults={'treasure': ', '.join(treasure)})
    # return redirect('/')


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
