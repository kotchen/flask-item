# import functools

# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db

# bp = Blueprint('canteens', __name__, url_prefix='/app')

# @bp.route('/canteens')
# def getCanteens():
#     db = get_db()
#     allCanteens = db.execute('SELECT * FROM map').fetchall()
#     return dict(allCanteens)

# @bp.route('/canteensPut',methods=['GET', 'POST'])
# def putCanteens():
#     if request.method == 'POST':
#         placename = request.json.get('placename')
#         num = request.json.get('num')
#         db = get_db()
#         error = None
#         if error is None:
#             db.execute(
#                 'INSERT INTO map (placename, num) VALUES (?, ?)',
#                 (placename, num)
#             )
#             db.commit()
#             return 'POST'
#         flash(error)
#     return 'GET'

