import datetime

from flask import render_template, request, redirect, send_from_directory, make_response

from app import app, ppoi_secret
from models import Point, Tag, PointTag, LogPoint, User, UserPoint
import requests
import json
from peewee import DoesNotExist


def checkPointGone(point_id, username):
    print(point_id, username)
    try:
        user = User.get(username=username)
        p = Point.get(id=point_id)
        UserPoint.get(point=p, user=user)
        return True
    except DoesNotExist:
        return False


app.jinja_env.globals.update(checkPointGone=checkPointGone)


#

@app.context_processor
def inject_user():
    username = request.cookies.get('username', False)
    if username:
        return dict(user=username)
    return {}


@app.route('/')
def homepage():
    x = Point.select().order_by(Point.created_date.desc()).execute()
    return render_template('index.html', points=x)


# def check_if_point_list_gone_and_bind_gone(points_list,username):
#     user=request.cookies.get('username',False)
#     for point in points_list:
#         userpo

@app.route('/gone', methods=['POST'])
def gone():
    point_id = request.form.get('point_id', False)
    user = request.cookies.get('username', False)
    if not user or not point_id:
        return 'nothing done'
    else:
        p = Point.get(id=point_id)
        u = User.get(username=user)
        try:
            u, _ = UserPoint.get_or_create(user=u, point=p)
            if not _:
                return 'nothing done'
            else:
                return 'success'
        except DoesNotExist:
            return 'nothing done'


@app.route('/nearest/<float:lon>/<float:lat>')
def nearest(lon, lat):
    x = list(Point.select().execute())  # type: list[Point]
    x.sort(key=lambda z: (float(z.longitude) - lon) ** 2 + (float(z.latitude) - lat) ** 2)
    return render_template('index.html', points=x)


@app.route('/ungone', methods=['POST'])
def ungone():
    point_id = request.form.get('point_id', False)
    user = request.cookies.get('username', False)
    if not user or not point_id:
        print('missing sth')
        return 'nothing done'
    else:
        try:
            p = Point.get(id=point_id)
            u = User.get(username=user)
            u = UserPoint.get(user=u, point=p)  # type: UserPoint
            u.delete_instance()
            return 'success'
        except DoesNotExist:
            return 'not exist'


@app.route('/filter.html')
def filter_():
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
    job_need_to_do = 256 * 4
    if request.method == 'GET':

        return render_template('register.html', workload=job_need_to_do, message='请不要使用移动设备,在点击验证码后别说我没提醒过..')
    elif request.method == 'POST':
        token = request.form.get('projectpoi-captcha-token')
        username = request.form.get('username')
        password = request.form.get('password')

        if (not username) or (not password):
            return render_template('register.html',
                                   workload=job_need_to_do,
                                   message='请填写用户名和密码')
        elif not token:
            return render_template('register.html',
                                   workload=job_need_to_do,
                                   message='你在搞笑吗')
        else:
            r = requests.post('https://api.ppoi.org/token/verify',
                              data={'secret': ppoi_secret,
                                    'token': token,
                                    'hashes': job_need_to_do})
            r = r.json()
            if r['success']:
                # create user here
                u, _ = User.get_or_create(username=username,
                                          defaults={
                                              'password': password,
                                              'mined': job_need_to_do,
                                              'ppoi_token': token})
                if not _:
                    return render_template('register.html',
                                           workload=job_need_to_do,
                                           message='用户名已经被别人用了')
                else:
                    r = make_response(redirect('/'))
                    r = set_login_cookies(r, u)
                    return r
            else:
                return render_template('register.html',
                                       workload=job_need_to_do,
                                       message='不要投机取巧哦')


def set_login_cookies(r, u):
    r.set_cookie('username', u.username, expires=datetime.datetime.today() + datetime.timedelta(days=3))
    return r


@app.route('/login', methods=['GET', 'POST'])
def login():
    job_need_to_do = 256 * 2
    if request.method == 'GET':
        return render_template('login.html', workload=job_need_to_do, message='请不要使用移动设备,在点击验证码后别说我没提醒过..')
    elif request.method == 'POST':
        token = request.form.get('projectpoi-captcha-token')
        username = request.form.get('username')
        password = request.form.get('password')

        if (not username) or (not password):
            return render_template('login.html',
                                   workload=job_need_to_do,
                                   message='请填写用户名和密码')
        elif not token:
            return render_template('login.html',
                                   workload=job_need_to_do,
                                   message='你在搞笑吗')
        else:
            r = requests.post('https://api.ppoi.org/token/verify',
                              data={'secret': ppoi_secret,
                                    'token': token,
                                    'hashes': job_need_to_do})
            r = r.json()
            if r['success']:
                # create user here
                try:
                    u = User.get(username=username,
                                 password=password)
                    r = make_response(redirect('/'))
                    r = set_login_cookies(r, u)
                    return r
                except User.DoesNotExist:
                    return render_template('login.html',
                                           workload=job_need_to_do,
                                           message='用户名或者密码错误')
            else:
                return render_template('login.html',
                                       workload=job_need_to_do,
                                       message='不要投机取巧哦')
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

    x, obj_created = Point.get_or_create(latitude=latitude,
                                         longitude=longitude,
                                         defaults={'treasure': ', '.join(treasure)})  # type:Point,bool
    if obj_created:
        for y in tags:
            PointTag.create(tag=y, point=x)
        l = LogPoint.create(latitude=latitude,
                            longitude=longitude,
                            treasure=', '.join(treasure),
                            created_date=x.created_date)
    else:
        return render_template('post.html', tags=Tag.select().execute(), message='坐标已存在')
        # return render_template('post.html')
        # return '坐标已存在 <a href="/post.html">重新分享</a>'
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


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
