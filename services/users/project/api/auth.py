# services/users/project/api/auth.py


from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User, School, Lesson, Site
from project import db, bcrypt
from project.api.constants import TEACHER, TECHNICIAN

from project.tests.utils import lesson_to_JSON

import pprint

auth_blueprint = Blueprint('auth', __name__)


pp = pprint.PrettyPrinter(indent=4)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()

    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(response_object), 400

    try:
        user_info = validate_new_user_details(post_data)
    except ValueError as e:
        response_object['message'] = str(e)
        return jsonify(response_object), 400
    # only people signing up a new school will register via this route

    user_info['admin'] = True

    try:
        # add new user to db
        new_user = User(user_info=user_info)
        db.session.add(new_user)
        db.session.commit()
        # generate auth token

        auth_token = new_user.encode_auth_token(new_user.id)

        response_object['status'] = 'success'
        response_object['message'] = 'Successfully registered.'
        response_object['user'] = new_user.asdict(exclude=['password'])
        response_object['user']['token'] = str(auth_token)

        return jsonify(response_object), 201

    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object['message'] = str(e)
        return jsonify(response_object), 400


def validate_new_user_details(post_data):

    user_info = {}

    if not post_data.get('email'):
        raise ValueError('No email provided.')

    user = User.query.filter(User.email == post_data.get('email')).first()
    if user:
        raise ValueError('That email is already taken.')

    else:
        user_info['email'] = post_data.get('email')

    if not post_data.get('name'):
        raise ValueError('No name provided.')
    else:
        user_info['name'] = post_data.get('name')

    if not post_data.get('password'):
        raise ValueError('No password provided.')
    else:
        user_info['password'] = post_data.get('password')

    if not post_data.get('role_code'):
        raise ValueError('No role code provided.')

    if int(post_data.get('role_code')) not in [TEACHER, TECHNICIAN]:
        raise ValueError('Role code must be 1 or 2.')

    user_info['role_code'] = post_data.get('role_code')

    # teachers MUST have staff codes
    if post_data.get('role_code') is TEACHER:
        if not post_data.get('staff_code'):
            raise ValueError('Teachers must have a staff code')

    if post_data.get('staff_code'):
        user_info['staff_code'] = post_data.get('staff_code')

    if post_data.get('school_id'):
        try:
            user_info['school_id'] = int(post_data.get('school_id'))
        except ValueError:
            raise ValueError('School ID must be integer.')

    return user_info


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                # response_object['auth_token'] = auth_token.decode()
                response_object['user'] = user.asdict()
                response_object['user']['token'] = auth_token.decode()
                school = School.query.get(user.school_id)
                try:
                    response_object['lessons'] = get_lessons(user)
                except ValueError as e:
                    pass
                if school:
                    response_object['school'] = school.asdict()
                    sites = Site.query.filter_by(school_id=school.id).all()
                    response_object['sites'] = [
                        site.asdict() for site in sites]
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception as e:
        print(str(e))
        response_object['message'] = str(e)
        return jsonify(response_object), 500


def get_lessons(user):
    lessons = [lesson_to_JSON(lesson) for lesson in Lesson.query.filter(
        Lesson.teacher_id == user.id).all()]
    if lessons:
        return lessons
    raise ValueError('No lessons')
