# services/users/project/api/users.py


from sqlalchemy import exc
from flask import Blueprint, jsonify, request
from project.api.models import Req, User, School, Lesson
from project import db
from project.api.utils import authenticate, get_role, \
    get_dates_for_get_reqs_request
from project.api.constants import TEACHER, TECHNICIAN, \
            TECHNICIAN_PATCH_AUTH, TEACHER_PATCH_AUTH,\
            DATETIME_FORMAT
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

    if get_role(resp) is TECHNICIAN:
        response_object['message'] = 'You do not have permission to do that.'
        return jsonify(response_object), 401

    if not post_data:
        return jsonify(response_object), 400

    user = User.query.get(int(resp))
    school = School.query.filter_by(id=user.school_id).first()

    title = post_data.get('title')
    equipment = post_data.get('equipment')
    notes = post_data.get('notes')
    time = datetime.strptime(post_data.get('time'), DATETIME_FORMAT)
    lesson_id = post_data.get('lesson_id')

    if time < datetime.now() + timedelta(
        days=school.preferences['days_notice']
    ):
        response_object = {
            'status': 'fail',
            'message': 'You cannot submit this req as it is less '
            'than {} days before it is due.'.format(
                school.preferences["days_notice"])
        }
        return jsonify(response_object), 401

    try:
        db.session.add(Req(
            title=title,
            equipment=equipment,
            notes=notes,
            time=time,
            user_id=resp,
            lesson_id=lesson_id,
            school_id=user.school_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = f'{title} was added!'
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


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

    if request.args.get('older'):
        try:
            older = int(request.args.get('older'))
        except ValueError:
            older = 0
    else:
        older = 0

    start_date, end_date = get_dates_for_get_reqs_request(older)

    if user.role_code is TEACHER:

        reqs = [
            req_to_JSON(req) for req in db.session.query(Req).
            filter(Req.user_id == user.id).
            filter(Req.time >= start_date).
            filter(Req.time <= end_date).
            all()
        ]

        lessons = [
            lesson_to_JSON(lesson) for lesson in db.session.query(Lesson).
            filter(Lesson.teacher_id == user.id)]

        reqs += lessons

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

    response_object = {
        'status': 'success',
        'data': {
            'reqs': reqs,
            'start_date': start_date,
            'end_date': end_date
        }
    }

    return jsonify(response_object), 200


@reqs_blueprint.route('/reqs/<req_id>', methods=['GET'])
def get_single_req(req_id):
    """Get single req details"""
    response_object = {
        'status': 'fail',
        'message': 'Req does not exist'
    }
    try:
        req = Req.query.filter_by(id=int(req_id)).first()
        if not req:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': req.to_json()
            }
            return jsonify(response_object), 200
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
