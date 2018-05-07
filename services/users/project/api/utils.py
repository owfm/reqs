# project/api/utils.py

from functools import wraps

from flask import request, jsonify

from project.api.models import User
from project.api.constants import ADMIN

from datetime import datetime, timedelta


def get_dates_for_get_reqs_request(weeks=0):
    '''

    Weeks will be positive or negative integer.

    If weeks = 1, return start and end date for NEXT week, if weeks = 2
    in 2 weeks etc. Weeks can be negative to get previous weeks.

    WEEKDAY INDEXES USE ISOWEEKDAY: MONDAY == 1

    '''

    today = datetime.now()

    most_recent_sunday = today - timedelta(days=today.isoweekday())

    if weeks == 0:
        start_date = most_recent_sunday - timedelta(weeks=4)
        end_date = today + timedelta(weeks=10)
    else:
        start_date = most_recent_sunday - timedelta(weeks=(4 * (older+1)))
        end_date = start_date + timedelta(days=27)

    return start_date, end_date


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), 401
        user = User.query.filter_by(id=resp).first()
        if not user:
            return jsonify(response_object), 401
        return f(resp, *args, **kwargs)
    return decorated_function


def authenticate_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), 401
        user = User.query.filter_by(id=resp).first()
        if not user:
            return jsonify(response_object), 401
        if user.role_code is not ADMIN:
            response_object['message'] = 'You must be admin to do that.'
            return jsonify(response_object), 401
        return f(resp, *args, **kwargs)
    return decorated_function


def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.admin


def get_role(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.role_code
