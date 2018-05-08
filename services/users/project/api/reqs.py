# services/users/project/api/users.py

from sqlalchemy import exc
from flask import Blueprint, jsonify, request
from project.api.models import Req, User, Lesson
from project import db
from project.api.utils import authenticate, \
    get_dates_for_get_reqs_request
from project.api.constants import TEACHER, TECHNICIAN,\
            TECHNICIAN_PATCH_AUTH, TEACHER_PATCH_AUTH,\
            DATE_FORMAT
from project.tests.utils import req_to_JSON, lesson_to_JSON
from jsonpatch import JsonPatch, InvalidJsonPatch
from jsondiff import diff
import pprint
from datetime import datetime, timedelta


reqs_blueprint = Blueprint('reqs', __name__)
pp = pprint.PrettyPrinter(indent=4)


@reqs_blueprint.route('/reqs', methods=['POST'])
@authenticate
def add_req(resp):

    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(response_object), 400

    user = User.query.get(int(resp))

    try:
        validate_new_req(post_data, user)
    except ValueError as e:
        response_object['message'] = str(e)
        return jsonify(response_object), 400

    try:
        new_req = create_new_req(post_data, user)
    except ValueError as e:
        response_object['message'] = str(e)
        return jsonify(response_object), 400

    try:
        db.session.add(new_req)
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = f'{new_req.title} was added!'
        response_object['data'] = req_to_JSON(new_req)
        return jsonify(response_object), 201
    except (exc.IntegrityError):
        db.session.rollback()
        return jsonify(response_object), 400


def validate_new_req(post_data, user):

    if not post_data.get('title'):
        raise ValueError('You must provide a title for your requisition.')

    if user.role_code is TECHNICIAN:
        raise ValueError('As a technician you cannot submit requisitions.')

    if not post_data.get('lesson_id'):
        raise ValueError('No lesson ID was provided.')
    try:
        datetime.strptime(post_data.get('currentWbDate'), DATE_FORMAT)
    except ValueError:
        raise ValueError('Submitted date improperly formatted.')


def create_new_req(post_data, user):
    title = post_data.get('title')
    equipment = post_data.get('equipment')
    notes = post_data.get('notes')
    week_beginning_date = post_data.get('currentWbDate')
    lesson_id = post_data.get('lesson_id')

    time = calculate_req_time(lesson_id, week_beginning_date)

    try:
        new_req = Req(
            title=title,
            equipment=equipment,
            notes=notes,
            time=time,
            user_id=user.id,
            lesson_id=lesson_id,
            school_id=user.school_id)
    except ValueError as e:
        raise ValueError(e)
    return new_req


def calculate_req_time(lesson_id, week_beginning_date):

    lesson = Lesson.query.get(lesson_id)
    date = datetime.strptime(week_beginning_date, DATE_FORMAT) +\
        timedelta(days=lesson.day_code-1)

    return datetime.combine(date, lesson.start_time)


@reqs_blueprint.route('/reqs', methods=['GET'])
@authenticate
def get_all_reqs(resp):

    '''

    if no query string, return reqs going back 4 weeks.

    If url contains 'older' query string with integer argument, return
    another 4 weeks of reqs from the previous month.

    Eg <url>/reqs/older=1 return reqs from 8 weeks ago to 4 weeks ago

    To avoid edge cases ensure all date sections begin on a Sunday and end
    on a Saturday.

    '''

    user = User.query.get(resp)

    if request.args.get('from') and request.args.get('to'):
        try:
            start_date = datetime.strptime(
                request.args.get('from'),
                DATE_FORMAT)
            end_date = datetime.strptime(
                request.args.get('to'),
                DATE_FORMAT)
        except Exception as e:
            response_object['status'] = 'fail'
            response_object['message'] = 'Date queries not provided or malformed.'
            response_object['error'] = str(e)
            return jsonify(response_object), 400

    reqs = get_sessions_helper(start_date, end_date, user)

    response_object = {
        'status': 'success',
        'data': {
            'reqs': reqs
        }
    }

    return jsonify(response_object), 200


def get_sessions_helper(start_date, end_date, user):
    if user.role_code is TEACHER:

        reqs = [
            req_to_JSON(req) for req in db.session.query(Req).
            filter(Req.user_id == user.id).
            filter(Req.time >= start_date).
            filter(Req.time <= end_date).
            all()
        ]

        # lessons = [
        #     lesson_to_JSON(lesson) for lesson in db.session.query(Lesson).
        #     filter(Lesson.teacher_id == user.id)]
        #
        # sessions += lessons

        # reqs.append([
        #     lesson_to_JSON(lesson) for lesson in db.session.query(Lesson).
        #     filter(Lesson.teacher_id == user.id)])

    else:
        reqs = [
            req_to_JSON(req) for req in db.session.query(Req).
            filter(Req.school_id == user.school_id).
            filter(Req.time >= start_date).
            filter(Req.time <= end_date).
            all()
        ]

    return reqs


@reqs_blueprint.route('/reqs/<req_id>', methods=['GET'])
@authenticate
def get_single_req(req_id):
    """Get single req details"""
    response_object = {
        'status': 'fail',
        'message': 'Req does not exist'
    }
    try:
        req = Req.query.get(req_id)
        if not req:
            return jsonify(response_object), 404

        if (user.role_code is TEACHER) and (req.user_id is user.id):
            response_object = {
                'status': 'success',
                'data': req.to_json()
            }
            return jsonify(response_object), 200

        if ((user.role_code is not TEACHER) and
                (req.school_id is user.school_id)):
                response_object = {
                    'status': 'success',
                    'data': req.to_json()
                }
                return jsonify(response_object), 200

        response_object['status'] = 'fail'
        response_object['message'] = 'That req is not yours to see.'
        return jsonify(response_object), 401

    except ValueError:
        return jsonify(response_object), 404


@reqs_blueprint.route('/reqs/<req_id>', methods=['PATCH'])
@authenticate
def update_single_requisition(resp, req_id):

    # teachers can edit their own requisitions
    # technicians can make their school's requisitions as done

    unauthorised = False

    response_object = {
        'status': 'fail',
        'message': 'Req does not exist'
    }

    user = User.query.get(resp)
    req = Req.query.get(req_id)

    if not req:
        return jsonify(response_object), 400

    # get patch object from client
    patch = JsonPatch(request.get_json())

    # convert target req object to dict to allow patching
    data = req.asdict(exclude_pk=True, exclude=['time'])

    # Apply the patch to the  dictionary instance of the model
    try:
        data_update = patch.apply(data)
    except InvalidJsonPatch:
        response_object = {
            'status': 'fail',
            'message': 'Malformed patch.'
        }
        return jsonify(response_object), 400

    change = diff(data, data_update)

    if not change:
        response_object = {
            'status': 'success',
            'message': 'Req {} unchanged.'.format(req.id)
            }
        return jsonify(response_object), 200

    if user.role_code is TEACHER:

        if req.isDone is True:
            response_object = {
                'status': 'fail',
                'message': 'Req {} has been marked as done '
                'and cannot be edited.'.format(req.id)
            }
            return jsonify(response_object), 401

        if req.user_id is not user.id:
            unauthorised = True

        for c in change:
            if c not in TEACHER_PATCH_AUTH:
                unauthorised = True

    elif user.role_code is TECHNICIAN:
        for c in change:
            if c not in TECHNICIAN_PATCH_AUTH:
                unauthorised = True

    if unauthorised:
        response_object = {
            'status': 'fail',
            'message': 'You are not authorised to do that.'
        }
        return jsonify(response_object), 401

    req.fromdict(data_update)
    db.session.commit()

    req = Req.query.get(req_id)

    response_object = {
        'status': 'success',
        'message': 'Req {} has been updated.'.format(req.id),
        'data': req_to_JSON(req)
    }
    return jsonify(response_object), 200


@reqs_blueprint.route('/reqs/<req_id>', methods=['DELETE'])
@authenticate
def delete_single_requisition(resp, req_id):

    # teachers can edit their own requisitions
    # technicians can make their school's requisitions as done

    response_object = {
        'status': 'fail',
        'message': 'Req does not exist.'
    }

    user = User.query.get(resp)
    req = Req.query.get(req_id)

    if not req:
        return jsonify(response_object), 404

    response_object = {
        'status': 'fail',
        'message': 'You are not authorised to do that.'
    }

# req exists

    if req.school_id is not user.school_id:
        return jsonify(response_object), 401

# req and user are same school

    if user.role_code == TEACHER and req.user_id != user.id:
        return jsonify(response_object), 401

# if teacher, own req: therefore can be deleted

    db.session.delete(req)
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Req {} has been deleted.'.format(req_id)
    }
    return jsonify(response_object), 200
