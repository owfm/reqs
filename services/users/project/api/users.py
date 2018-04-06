# services/users/project/api/users.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from project.api.models import User, School
from project import db
from project.api.utils import authenticate, authenticate_admin
from project.api.constants import ADMIN

import pprint

pp = pprint.PrettyPrinter(indent=4)

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/checkemail', methods=['POST'])
def check_email():

    ''' checks to see if an email exists in database '''

    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }

    if not post_data:
        return jsonify(response_object)
    email = post_data.get('email')
    try:
        user = User.query.filter(User.email == email).first()
        if not user:
            response_object['status'] = 'success'
            response_object['message'] = 'User not found.'
            return jsonify(response_object), 200
        else:
            response_object['status'] = 'success'
            response_object['message'] = 'User found.'
            return jsonify(response_object), 200

    except ValueError as e:
        return jsonify(response_object), 400


@users_blueprint.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong!'})


@users_blueprint.route('/register', methods=['POST'])
def register_admin():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(response_object), 400

    name = post_data.get('name')
    email = post_data.get('email')
    password = post_data.get('password')
    staff_code = post_data.get('staff_code')
    school_name = post_data.get('school_name')

    try:
        school = School.query.filter_by(name=school_name).first()
        if not school:
            db.session.add(School(name=school_name))
            db.session.commit()
    except exc.IntegrityError as e:
        db.session.rolleback()
        response_object['message'] = "Sorry. That school already exists."
        return jsonify(response_object), 400

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                name=name,
                email=email,
                password=password,
                role_code=ADMIN,
                school_id=school.id,
                staff_code=staff_code))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route('/users/me', methods=['GET'])
@authenticate
def get_self(resp):

    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.get(int(resp))
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'message': 'User found.',
                'data': user.asdict()
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
@authenticate_admin
def test_get_all_users(resp):

    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }

    user = User.query.get(int(resp))

    if not user:
        return jsonify(response_object), 404

    try:
        school = School.query.get(user.school_id)
    except Exception as e:
        response_object['message'] = 'Error finding school.'

        return jsonify(response_object), 404

    response_object = {
        'status': 'success',
        'data': {
            'users': [user.asdict() for user in User.query.filter_by(
                school_id=school.id).all()]
        }
    }
    return jsonify(response_object), 200
