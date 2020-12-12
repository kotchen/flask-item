import functools
import json
import base64
import os
import enum
# import numpy as np
# import cv2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

class CN(enum.IntEnum):
    一食堂,二食堂,三食堂,四食堂,五食堂,六食堂,七食堂,八食堂,九食堂,十食堂 = range(10)

bp = Blueprint('auth', __name__, url_prefix='/app')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
        
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # username = request.json.get('username')
        # password = request.json.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
            #return dict(user='checked',user_name=user['username'])
        flash(error)
        #return dict(user='unchecked',identity='empty')
    return render_template('auth/login.html')

@bp.route('/canteens')
def getCanteens():
    db = get_db()
    allCanteens = db.execute('SELECT * FROM map'
                            #'order by num DESC'
    ).fetchall()
    info = {}
    data = json.loads(json.dumps(info))
    data['canteens'] = dict(allCanteens)
    return data

@bp.route('/canteensPut',methods=['GET', 'POST'])
def putCanteens():
    if request.method == 'POST':
        placename = request.json.get('placename')
        num = request.json.get('num')
        db = get_db()
        if db.execute(
            'SELECT placename FROM map WHERE placename = ?', (placename,)
        ).fetchone() is None:
            db.execute(
                'INSERT INTO map (placename, num) VALUES (?, ?)',
                (placename, num)
            )
            db.commit()
            return 'POST'
        else:
            db.execute('UPDATE map SET num = ? WHERE placename = ?',(num,placename))
            db.commit()
            return 'POST'
    return 'GET'

@bp.route('/canteens/canteen&<int:i>')
def getWins(i):
    db = get_db()
    placename = "食堂" + str(i)
    allWindows = db.execute(
            'SELECT * FROM windows WHERE placename = ?', (placename,)
        ).fetchone()
    info = {}
    data = json.loads(json.dumps(info))
    win = {}
    win["窗口一"] = allWindows['windowsOneNum']
    win["窗口二"] = allWindows['windowsTwoNum']
    data[placename] = win
    return data

@bp.route('/winPut',methods=['GET', 'POST'])
def putWin():
    if request.method == 'POST':
        placename = request.json.get('placename')
        num1 = request.json.get('num1')
        num2 = request.json.get('num2')
        db = get_db()
        if db.execute(
            'SELECT placename FROM windows WHERE placename = ?', (placename,)
        ).fetchone() is None:
            db.execute(
                'INSERT INTO windows (placename, windowsOneNum, windowsTwoNum) VALUES (?, ?, ?)',
                (placename, num1, num2)
            )
            db.commit()
            return 'POST1'
        else:
            db.execute('UPDATE windows SET windowsOneNum = ?, windowsTwoNum = ? WHERE placename = ?',(num1,num2,placename))
            db.commit()
            return 'POST2'
    return 'GET'

@bp.route('/canteens/canteen&<int:i>/window_name&<int:j>.jpg')
def sendPicture(i,j):
    path = os.getcwd() + str(i) + 'windows' + str(j) + '.jpg'
    image = open(path,'rb')
    resp = Response(image, mimetype="i/jpeg")
    return resp

@bp.route('/getPicture',methods=['GET', 'POST'])
def getPicture():
    if request.method == 'POST':
        path = os.getcwd()
        canteen = request.json.get('canteen')
        imgStr_1 = request.json.get('window_1')
        imgStr_2 = request.json.get('window_2')
        img_decode_1 = imgStr_1.encode('ascii')  # ascii编码
        img_decode_1_ = base64.b64decode(img_decode_1)  # base64解码
        img_decode_2 = imgStr_2.encode('ascii')  # ascii编码
        img_decode_2_ = base64.b64decode(img_decode_2)  # base64解码
        file = open(path+canteen+'windows1.jpg','wb')
        file.write(img_decode_1_)
        file.close()
        file = open(path+canteen+'windows2.jpg','wb')
        file.write(img_decode_2_)
        file.close()
        return 'post'
    return 'GET'

@bp.route('/canteens/canteen&<int:i>/menu')
def get_menu(i):
    db = get_db()
    placename = "食堂"+ str(i)
    allmenu = db.execute(
            'SELECT * FROM menu WHERE placename = ?', (placename,)
        ).fetchone()
    allmenuDict = dict(allmenu)
    del allmenuDict['placename']
    info = {}
    data = json.loads(json.dumps(info))
    data[placename] = allmenuDict
    return data

@bp.route('/menuPut',methods=['GET', 'POST'])
def putMenu():
    if request.method == 'POST':
        placename = request.json.get('placename')
        menu1 = request.json.get('menu1')
        menu2 = request.json.get('menu2')
        menu3 = request.json.get('menu3')
        menu4 = request.json.get('menu4')
        db = get_db()
        if db.execute(
            'SELECT placename FROM menu WHERE placename = ?', (placename,)
        ).fetchone() is None:
            db.execute(
                'INSERT INTO menu (placename, menu1, menu2, menu3, menu4) VALUES (?, ?, ?, ?, ?)',
                (placename, menu1, menu2, menu3, menu4)
            )
            db.commit()
            return 'POST1'
        else:
            db.execute('UPDATE menu SET menu1 = ?, menu2 = ?, menu3 = ?, menu4 = ? WHERE placename = ?',(menu1,menu2,menu3,menu4,placename))
            db.commit()
            return 'POST2'
    return 'GET'

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str