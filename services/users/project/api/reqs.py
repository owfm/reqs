# services/users/project/api/users.py

from sqlalchemy import exc
from flask import Blueprint, jsonify, request
from project.api.models import Req, User, Lesson, School
from project import db
from project.api.utils import authenticate
from project.api.constants import TEACHER, TECHNICIAN,\
            TECHNICIAN_PATCH_AUTH, TEACHER_PATCH_AUTH,\
            DATE_FORMAT, TIMESTAMP_FORMAT
from project.tests.utils import req_to_JSON
from project.api.school_utils import get_week_number
from jsonpatch import JsonPatch, InvalidJsonPatch
from jsondiff import diff
import pprint
from datetime import datetime, time, date, timedelta


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
        datetime.strptime(post_data.get('currentWbStamp'), DATE_FORMAT)
    except ValueError:
        raise ValueError('Submitted date improperly formatted.')


def create_new_req(post_data, user):
    title = post_data.get('title')
    equipment = post_data.get('equipment')
    notes = post_data.get('notes')
    week_beginning_date = post_data.get('currentWbStamp')
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

    user = User.query.get(resp)

    response_object = {}

    try:
        reqs, week_number = parse_reqs_query_arguments(request.args, user)
    except ValueError as e:
        print(str(e))
        response_object['status'] = 'fail'
        response_object['message'] = str(e)
        return jsonify(response_object), 400

    response_object['status'] = 'success'

    response_object['items'] = reqs

    response_object['weeknumber'] = week_number

    return jsonify(response_object), 200


def parse_reqs_query_arguments(request_args, user):

    if not request_args.get('wb'):
        raise ValueError('Please provide week beginning date query.')

    try:
        wb = datetime.strptime(request_args.get('wb'), DATE_FORMAT)
    except ValueError as e:
        raise ValueError(e)

    if wb.isoweekday() is not 1:
        raise ValueError('Supplied date is not a Monday.')

    # create from - to datetime objects to cover whole week
    from_datetime = datetime.combine(wb.date(), time.min)
    to_datetime = datetime.combine((wb.date() + timedelta(days=6)), time.max)

    query = db.session.query(Req).filter(
        Req.school_id == user.school_id,
        Req.time > from_datetime,
        Req.time < to_datetime)

    if request_args.get('lastupdated'):
        try:
            last_updated = datetime.strptime(
                request_args.get('lastupdated'), TIMESTAMP_FORMAT)
            query = query.filter(Req.last_updated > last_updated)
        except ValueError:
            pass

    # if teacher, filter reqs to only give own reqs unless 'all' query supplied

    all = True if request_args.get('all') == 'true' else False

    if user.role_code == TEACHER and not all:
        query = query.filter(Req.user_id == user.id)

    school = School.query.get(user.school_id)

    try:
        week_number = get_week_number(wb, school.preferences)
    except ValueError as e:
        raise ValueError(e)

    return [req_to_JSON(req) for req in query], week_number


@reqs_blueprint.route('/reqs/<req_id>', methods=['GET'])
@authenticate
def get_single_req(resp, req_id):

    user = User.query.get(resp)

    """Get single req details"""
    response_object = {
        'status': 'fail',
        'message': 'Req does not exist'
    }
    req = Req.query.get(req_id)
    if not req:
        return jsonify(response_object), 404

    if req.user_id is user.id:
        response_object = {
            'status': 'success',
            'data': req_to_JSON(req)
        }
        return jsonify(response_object), 200

    if ((user.role_code is TECHNICIAN) and (req.school_id is user.school_id)):
        response_object = {
            'status': 'success',
            'data': req_to_JSON(req)
        }
        return jsonify(response_object), 200

    response_object['status'] = 'fail'
    response_object['message'] = 'Unauthorised.'
    return jsonify(response_object), 401


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
    req.last_updated = datetime.now()
    db.session.commit()

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
