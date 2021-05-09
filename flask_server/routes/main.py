import json
from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required

from flask_server.extensions import db
from flask_server.models import User, Messages

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return '{ Welcome to messaging system, By: Sapir Nahum }'

@main.route('/write_msg', methods=['GET', 'POST'])
@login_required
def write_msg():
    if request.method == 'POST':
        new_mes = Messages(
            sender=current_user.name,
            receiver=request.args.get('receiver', default=None, type=str),
            message = request.args.get('message', default=None, type=str),
            subject = request.args.get('subject', default=None, type=str),
            date = date.today()
        )
        db.session.add(new_mes)
        db.session.commit()
    return '{ status : message sent }'

@main.route('/get_messages', methods=['GET', 'POST'])
@login_required
def get_messages():
    user = current_user.name
    messages = Messages.query.filter_by(receiver=user).all()
    return jsonify(messages)

@main.route('/get_unread_messages', methods=['GET', 'POST'])
@login_required
def get_unread_messages():
    user = current_user.name
    messages = Messages.query.filter_by(receiver=user,opened=False).all()
    return jsonify(messages)


@main.route('/delete_msg/<int:msg_id>')
@login_required
def delete_msg(msg_id):
    Messages.query.filter_by(id=msg_id).delete()
    db.session.commit()
    return 'message deleted successfully'


@main.route('/open_msg/<int:msg_id>')
@login_required
def open_msg(msg_id):
    msg = Messages.query.get_or_404(msg_id)
    msg.opened = True
    db.session.commit()

    return json.dump(msg)