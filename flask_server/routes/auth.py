from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask_server.extensions import db
from flask_server.models import Messages, User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user_name = request.args.get('user_name', default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        user = User(
            name=user_name,
            unhashed_password=password,
        )
        db.session.add(user)
        db.session.commit()

        return '{ register_status : success,\nuser : ' + user_name + ',\npassword : ' + password + ' }'
    return '{ register_status : failed }'


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        next = request.args.get('next', default=None, type=str)
        if next != None:
            return '{ login is required }'
    if request.method == 'POST':
        user_name = request.args.get('user_name', default=None, type=str)
        password = request.args.get('password', default=None, type=str)
        user = User.query.filter_by(name=user_name).first()
        error_message = ''

        if not user or not check_password_hash(user.password, password):
            error_message = 'Could not login. Please check and try again.'
            return '{ login_status : failed,\nerror : ' + error_message + ' }'

        if not error_message:
            login_user(user)
            return '{ login_status : success }'

    return '{ login_status : failed }'


@auth.route('/logout',methods=['POST'])
def logout():
    logout_user()
    return '{ logout_status : success }'
