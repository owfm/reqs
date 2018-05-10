# services/users/project/api/auth.py


from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User, School, Lesson
from project import db, bcrypt
from project.api.constants import ADMIN

from project.tests.utils import lesson_to_JSON


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        response_object['logging'] = 'no post data'
        return jsonify(response_object), 400
    name = post_data.get('name')
    email = post_data.get('email')
    password = post_data.get('password')
    # role_code = post_data.get('role_code')
    staff_code = post_data.get('staff_code')
    school_id = post_data.get('school_id')

    try:
        user = User.query.filter(User.email == email).first()
        if not user:
            # add new user to db
            new_user = User(
                name=name,
                email=email,
                password=password,
                role_code=ADMIN,
                staff_code=staff_code,
                school_id=school_id
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully registered.'
            response_object['user'] = new_user.asdict(exclude=['password'])
            response_object['user']['token'] = auth_token
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That user already exists.'
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


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
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception as e:
        print(str(e))
        response_object['message'] = 'Try again.'
        return jsonify(response_object), 500

def get_lessons(user):
    lessons = [lesson_to_JSON(lesson) for lesson in Lesson.query.filter(
        Lesson.teacher_id==user.id).all()]
    if lessons:
        return lessons
    raise ValueError('No lessons')

@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    # get auth token
    auth_header = request.headers.get('Authorization')
    response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            if not user:
                return jsonify(response_object), 401
            else:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged out.'
                return jsonify(response_object), 200
        else:
            response_object['message'] = resp
            return jsonify(response_object), 401
    else:
        return jsonify(response_object), 403
