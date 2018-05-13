from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from jsonpatch import JsonPatch, JsonPatchException, JsonPatchConflict
from jsondiff import diff
import pprint
from datetime import datetime
import re

from project import db

from project.api.models import User, School, Site
from project.tests.utils import add_user
from project.api.excel import extract_users
from project.api.school_utils import process_preferences, get_week_number
from project.api.utils import authenticate, authenticate_admin
from project.api.constants import TEACHER, DATE_FORMAT,\
    TIME_FORMAT, EDITABLE_PREFERENCES


school_blueprint = Blueprint('school', __name__)
pp = pprint.PrettyPrinter(indent=4)


@school_blueprint.route('/schools/check', methods=['GET'])
@authenticate
def get_week_number_route(resp):

    user = User.query.get(resp)
    school = School.query.get(user.school_id)

    response_object = {
        'status': 'fail'
    }

    if request.args.get('date'):
        try:
            date = str(request.args.get('date'))
        except ValueError:
            response_object['message'] = 'No date query provided.'
            return jsonify(response_object), 400
    try:
        week_number = get_week_number(date, school.preferences)
    except BaseException as e:
        response_object['message'] = str(e)
        return jsonify(response_object), 400

    response_object = {
        'status': 'success',
        'data': week_number
    }
    return jsonify(response_object), 200


@school_blueprint.route('/schools', methods=["GET"])
@authenticate
def get_school(resp):

    user = User.query.get(resp)
    school = School.query.get(user.school_id)

    response_object = {
        'status': 'fail',
        'message': 'School doesn\'t exist or not assigned to user.'
    }

    if not school:
        return jsonify(response_object), 404

    sites = Site.query.filter_by(school_id=school.id).all()

    data = school.asdict()
    if sites:
        data['sites'] = [site.asdict() for site in sites]

    response_object = {
        'status': 'success',
        'message': 'Found school.',
        'data': data
    }

    return jsonify(response_object), 200


@school_blueprint.route('/schools', methods=["POST"])
@authenticate_admin
def add_school(resp):

    user = User.query.get(resp)

    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    post_data = request.get_json()

    if not post_data:
        return jsonify(response_object), 400

    name = post_data['name']

    new_school = School(
        name=name
    )
    try:
        db.session.add(new_school)
        db.session.flush()
        user.school_id = new_school.id
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': '{} has been created.'.format(name),
            'data': new_school.asdict()
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400


@school_blueprint.route('/schools/preferences', methods=['PATCH'])
@authenticate_admin
def update_school_preferences(resp):

    response_object = {
        'status': 'fail',
        'message': 'School does not exist.'
    }

    user = User.query.get(resp)
    school = School.query.get(user.school_id)

    if not school:
        return jsonify(response_object), 400

    response_object = {
        'status': 'fail',
        'message': 'Malformed patch.'
    }

    # get patch object from client
    patch_raw = request.get_json()

    if not patch_raw or not isinstance(patch_raw, list):
        return jsonify(response_object), 400

    # for any times or dates in the patch object, check correct formatting
    for edit in patch_raw:
        try:
            if str(edit['path']) not in EDITABLE_PREFERENCES:
                return jsonify(response_object), 400
        except KeyError:
            return jsonify(response_object), 400

        if edit['path'] == '/term_dates':
            for halfterm in edit['value']:  # dict
                try:
                    datetime.strptime(
                        halfterm[0], DATE_FORMAT)
                    datetime.strptime(
                        halfterm[1], DATE_FORMAT
                    )
                except ValueError:
                    return jsonify(response_object), 400

        elif edit['path'] == '/period_start_times':
            for period in edit['value']:
                try:
                    datetime.strptime(
                        edit['value'][period], TIME_FORMAT)
                except ValueError:
                    return jsonify(response_object), 400

        elif edit['path'] == '/period_length_in_minutes':
            try:
                int(edit['value'])
            except ValueError as e:
                response_object['message'] = str(e)
                return jsonify(response_object), 400

        elif edit['path'] == '/weeks_timetable':
            try:
                assert int(edit['value']) in [1, 2]

            except(AssertionError):
                return jsonify(response_object), 400
            except(ValueError):
                return jsonify(response_object), 400

        elif edit['path'] == '/days_notice':
            try:
                int(edit['value'])
            except ValueError:
                return jsonify(response_object), 400

    # convert raw JSON from client into JSONPatch format
    patch = JsonPatch(patch_raw)

    # get preferences JSON object from school
    preferences = school.preferences

    # Apply the patch to the dictionary instance of the model
    try:
        preferences_update = patch.apply(preferences)
    except (JsonPatchConflict, JsonPatchException):
        return jsonify(response_object), 400

    change = diff(preferences, preferences_update)

    if not change:
        response_object = {
            'status': 'success',
            'message': '{} preferences unchanged.'.format(school.name)
            }
        return jsonify(response_object), 200

    # check new preferences object for consistency, and process
    try:
        response_object = process_preferences(preferences_update)
    except BaseException as e:
        response_object = {
            'status': 'fail',
            'message': e
        }

    school.preferences = preferences_update
    db.session.commit()

    response_object = {
        'status': 'success',
        'message': 'Preferences for {} have been updated.'.format(school.name),
        'data': {'school': school.asdict()}
    }
    return jsonify(response_object), 200


@school_blueprint.route('/schools/<school_id>/staff', methods=['POST'])
@authenticate_admin
def prepare_staff_accounts(resp, school_id):

    school = School.query.get(school_id)

    if not school:
        response_object = {
            'status': 'fail',
            'message': 'That school does not exist.'
        }
        return jsonify(response_object), 401

    filename = request.get_json()

    if not filename:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 401

    wb_staff, staff = extract_users(filename['filename'])

    # will return string error code if doesn't work - check, then return
    if isinstance(staff, str):
        response_object = {
            'status': 'fail',
            'message': staff
        }
        return jsonify(response_object), 401

    """ PERFORM CHECKS ON EXTRACTED DATA """

    response_object = {
        'status': 'fail',
        'message': 'User import failed'
    }

    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    for staff_member in staff:
        if not EMAIL_REGEX.match(staff_member['email']):
            response_object['message'] = 'Emails are incorrect.'
            return jsonify(response_object), 401
        if staff_member['name'] is None:
            response_object['message'] = (
                'Names are missing from the uploaded file.')
            return jsonify(response_object), 401
        if (staff_member['staff_code'] is None
                and staff_member['role_code'] is TEACHER):
            response_object['message'] = (
                'Staff codes are missing from the uploaded file.')
            return jsonify(response_object), 401

    # get list of emails already signed up to the school, to ensure imported
    # emails are unique without raising db Exception

    emails = [user.email for user in User.query.filter_by(
        school_id=school_id).all()]

    skipped_emails = []
    for s in staff:
        # skip any emails already in database
        if s['email'] in emails:
            skipped_emails.append(s['email'])
            continue

        new_user = add_user(
                        name=s['name'], email=s['email'],
                        password='password', role_code=s['role_code'],
                        staff_code=s['staff_code'], school_id=school.id)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return jsonify({'status': 'fail', 'message': str(e)}), 401

    # if emails needed to be skipped (admin should be one) send list in
    # warning message of response dict
    if len(skipped_emails) > 0:
        response_object['warning'] = {'skipped_users': skipped_emails}

    response_object['status'] = 'success'
    response_object['data'] = \
        {'staff': [user.asdict() for user in User.query.filter_by(
            school_id=school.id).all()]}
    response_object['message'] = 'Please ensure these users are correct.'

    return jsonify(response_object), 200
