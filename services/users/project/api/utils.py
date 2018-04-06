# project/api/utils.py

from functools import wraps

from flask import request, jsonify

from project.api.models import User
from project.api.constants import ADMIN

from datetime import datetime, timedelta


def get_dates_for_get_reqs_request(older=0):
    '''

    If older argument is supplied, returns dates going back in multiples
    of 4 weeks.

    eg: older = 0: from monday 4 weeks ago until 10 weeks in the future (
    essentially ensuring all recent requisitions will be returned
    )
    older = 1: from monday 8 weeks ago for 4 full weeks i.e. until the Friday
    25 days later.

    Counting back starts from today if called on a Monday, otherwise most
    recent Monday.

    WEEKDAY INDEXES USE ISOWEEKDAY: MONDAY == 1

    '''

    today = datetime.now()

    most_recent_sunday = today - timedelta(days=today.isoweekday())

    if older == 0:
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
