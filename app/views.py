from flask import render_template, request, redirect

from app import app
from models import Point


@app.route('/')
def homepage():
    x = Point.select().order_by(Point.created_date.desc()).execute()
    # print(x.__dict__)
    return render_template('index.html', points=x)


@app.route('/post', methods=["POST"])
def post():
    longitude = request.form.get('longitude', '')
    latitude = request.form.get('latitude', '')
    treasure = request.form.getlist('treasure')
    Point.get_or_create(latitude=latitude, longitude=longitude,
                        defaults={'treasure': ', '.join(treasure)})
    return redirect('/')
