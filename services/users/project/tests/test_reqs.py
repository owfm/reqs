import json

from datetime import datetime, timedelta

from project import db
from project.api.models import Req, User, School
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_req, add_school
from project.api.constants import TEACHER, TECHNICIAN, DATETIME_FORMAT
from project.api.reqs import calculate_req_time
from project.tests.utils import populate_school_db, populate_school_with_reqs


import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestReqService(BaseTestCase):
    """Tests for the Req Service."""
    def test_calculate_req_time(self):

        school = School(name='Holy Family Catholic School')
        db.session.add(school)
        db.session.commit()

        populate_school_db(school.id)

        populate_school_with_reqs(school.id)

        db.session.add(School(name='testSchool'))

        db.session.commit()

        time = calculate_req_time(161, '16-04-18')
        print(time)

    def test_add_req(self):
        """Ensure a new req can be added to the database."""
        school = add_school('testschool')

        add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)

        now = datetime.now() + timedelta(days=10)
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'lesson_id': 1,
                    'time': datetime.strftime(now, DATETIME_FORMAT)
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('reqtitletest was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_req_no_title(self):

        """ensure post req with no title raises exception"""

        school = add_school('testschool')
        add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id
        )

        now = datetime.now() + timedelta(days=10)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'time': datetime.strftime(now, DATETIME_FORMAT)
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_has_correct_user_and_school_id(self):
        """Ensure a new req gets correct user_id from auth token."""

        school = add_school('testschool')

        user = add_user('ollie mansell', 'test@test.com', 'olliepass',
                        TEACHER, 'MAO', school.id)

        now = datetime.now() + timedelta(days=10)
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            resp = User.decode_auth_token(token)

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'time': datetime.strftime(now, DATETIME_FORMAT)
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )

            new_req = Req.query.filter_by(title='reqtitletest').first()
            user = User.query.filter_by(id=int(resp)).first()

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('reqtitletest was added!', data['message'])
            self.assertEqual(new_req.user_id, user.id)
            self.assertEqual(new_req.school_id, user.school_id)
            self.assertIn('success', data['status'])

    def test_add_req_invalid_json(self):
        """ensure post req with no school_id raises exception"""

        school = add_school('testschool')
        add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id
        )

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_no_token(self):
        """ensure can't post req without valid login token"""

        school = add_school('testschool')
        user = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)

        now = datetime.now() + timedelta(days=10)

        with self.client:
            self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'time': datetime.strftime(now, DATETIME_FORMAT),
                    'user_id': user.id,
                    'school_id': school.id
                }),
                content_type='application/json'
                # headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Provide a valid auth token.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_not_logged_in(self):
        """ensure can't post req without being logged in"""

        school = add_school('testschool')
        user = add_user('ollie mansell', 'test@test.com', 'olliepass',
                        TEACHER, 'MAO', school.id)

        now = datetime.now() + timedelta(days=10)

        with self.client:
            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'time': datetime.strftime(now, DATETIME_FORMAT),
                    'user_id': user.id,
                    'school_id': school.id
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Provide a valid auth token.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_technician(self):
        """ ensure can't post req as technician"""

        school = add_school('testschool')

        user = add_user('ollie mansell', 'test@test.com', 'olliepass',
                        TECHNICIAN, 'MAO', school.id)

        now = datetime.now() + timedelta(days=10)
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'time': datetime.strftime(now, DATETIME_FORMAT),
                    'user_id': user.id,
                    'school_id': school.id
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You do not have permission to do that.',
                data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_too_late(self):
        """ Ensure you can't post req later than
        lead-time specified in school preferences """

        school = add_school('testschool')
        school.preferences["days_notice"] = 3

        user = add_user('ollie mansell', 'test@test.com', 'olliepass',
                        TEACHER, 'MAO', school.id)

        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'time': datetime.strftime(
                        datetime.now() +
                        timedelta(days=2), DATETIME_FORMAT),
                    'user_id': user.id,
                    'school_id': school.id
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You cannot submit this req as it is less '
                'than {} days before it is due.'.
                format(school.preferences["days_notice"]),
                data['message'])
            self.assertIn('fail', data['status'])

    def test_mark_req_as_done(self):
        """ensure technician can mark req as done"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test2@test.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps([{
                    "op": "replace",
                    "path": "/isDone", "value": True}]),
                headers={'Authorization': f'Bearer {token}'}
            )

            req_from_db = Req.query.get(req.id)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                'Req {} has been updated.'.format(req.id),
                data['message'])
            self.assertEqual(req_from_db.isDone, True)
            self.assertIn('success', data['status'])

    def test_mark_req_as_done_fails_malformed_patch(self):
        """ensure technician can mark req as done"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)

        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id
        )

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test2@test.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps([{}]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Malformed patch.'.format(req.id), data['message'])
            self.assertIn('fail', data['status'])

    def test_unchanged_req(self):
        """ensure correct response if req is unchanged"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)

        req.isDone = True

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test2@test.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps(
                    [{"op": "replace", "path": "/isDone", "value": True}]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Req {} unchanged.'.format(req.id), data['message'])
            self.assertIn('success', data['status'])

    def test_req_marked_done_by_teacher(self):
        """ensure correct response if req is marked done by a teacher"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)
        req.isDone = False

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            User.decode_auth_token(token)

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps(
                    [{"op": "replace", "path": "/isDone", "value": True}]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You are not authorised to do that.', data['message'])
            self.assertIn('fail', data['status'])

    def test_req_marked_hasIssue_by_teacher(self):
        """ensure correct response if req
        is marked as having issue by a teacher"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)

        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now, teacher.id,
            school.id)
        req.hasIssue = False

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps(
                    [{"op": "replace", "path": "/hasIssue", "value": True}]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You are not authorised to do that.', data['message'])
            self.assertIn('fail', data['status'])

    def test_req_edit_by_teacher(self):
        """ensure correct response if req is edited by a teacher"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)
        req.hasIssue = False

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps([
                    {"op": "replace", "path": "/title", "value": "new title"},
                    {"op": "replace", "path": "/equipment",
                        "value": "new equipment"},
                    {"op": "replace", "path": "/notes",
                        "value": "new notes"}
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            req_from_db = Req.query.get(req.id)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(req_from_db.title, "new title")
            self.assertEqual(req_from_db.equipment, "new equipment")
            self.assertEqual(req_from_db.notes, "new notes")
            self.assertIn(
                'Req {} has been updated.'.format(req_from_db.id),
                data['message'])
            self.assertIn('success', data['status'])

    def test_req_edit_by_technician(self):
        """ensure correct response if req is edited by a technician"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)
        req.hasIssue = False

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test2@test.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps([
                    {"op": "replace", "path": "/title", "value": "new title"},
                    {"op": "replace", "path": "/equipment",
                        "value": "new equipment"},
                    {"op": "replace", "path": "/notes", "value": "new notes"}
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            req_from_db = Req.query.get(req.id)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(req_from_db.title, "title")
            self.assertEqual(req_from_db.equipment, "equipment")
            self.assertEqual(req_from_db.notes, "notes")
            self.assertIn(
                'You are not authorised to do that.', data['message'])
            self.assertIn('fail', data['status'])

    def test_req_edit_by_teacher_after_marked_done(self):
        """ensure correct response if req is edited by a
        teacher after marked as done"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell', 'test@test.com', 'olliepass', TEACHER, 'MAO',
            school.id)
        add_user(
            'gary tyler', 'test2@test.com', 'garypass', TECHNICIAN, 'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title", "equipment", "notes", now, teacher.id, school.id)
        req.isDone = True

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps([
                    {"op": "replace", "path": "/title", "value": "new title"},
                    {"op": "replace", "path": "/equipment",
                        "value": "new equipment"},
                    {"op": "replace", "path": "/notes", "value": "new notes"}
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            req_from_db = Req.query.get(req.id)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(req_from_db.title, "title")
            self.assertEqual(req_from_db.equipment, "equipment")
            self.assertEqual(req_from_db.notes, "notes")
            self.assertIn(
                'Req {} has been marked as done and cannot be edited.'.
                format(req_from_db.id), data['message'])
            self.assertIn('fail', data['status'])

    def test_req_edit_by_teacher_not_owned_by_teacher(self):
        """ensure correct response if req is edited by a
         teacher who doesn't own it"""

        school = add_school(name='testschool')

        add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id
        )
        teacher2 = add_user(
            'oliver keers',
            'keo@keo.com',
            'keerspass',
            TEACHER,
            'KEO',
            school.id)

        req = add_req(
            "title", "equipment", "notes", datetime.now(),
            teacher2.id, school.id
        )

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.patch(
                '/reqs/' + str(req.id),
                content_type='application/json',
                data=json.dumps([
                    {"op": "replace", "path": "/title", "value": "new title"},
                    {"op": "replace", "path": "/equipment",
                        "value": "new equipment"},
                    {"op": "replace", "path": "/notes", "value": "new notes"}
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            req_from_db = Req.query.get(req.id)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            # ensure req is unchanged
            self.assertEqual(req_from_db.title, "title")
            self.assertEqual(req_from_db.equipment, "equipment")
            self.assertEqual(req_from_db.notes, "notes")
            self.assertIn(
                'You are not authorised to do that.'.
                format(req_from_db.id), data['message']
            )
            self.assertIn('fail', data['status'])

    def test_get_own_reqs_as_teacher(self):

        """ensure get /reqs as teacher returns that teachers reqs only"""
        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id
        )
        teacher2 = add_user(
            'oliver keers',
            'keo@keo.com',
            'keerspass',
            TEACHER,
            'KEO',
            school.id
        )

        now = datetime.now() + timedelta(days=5)

        add_req(
            "title1",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)

        add_req(
            "title2",
            "equipment2",
            "notes2",
            now,
            teacher.id,
            school.id
        )

        add_req(
            "title3",
            "equipment3",
            "notes3",
            now,
            teacher2.id,
            school.id
        )
        add_req(
            "title4",
            "equipment4",
            "notes4",
            now,
            teacher2.id,
            school.id
        )

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/reqs',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['reqs']), 2)

            for req in data['data']['reqs']:
                self.assertEqual(req['user_id'], teacher.id)

            self.assertIn('success', data['status'])

    def test_get_schools_reqs_as_technician(self):
        """ensure get /reqs as technician returns that schools reqs only"""

        school1 = add_school(name='testschool')
        school2 = add_school(name='testschool2')

        teacher1 = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school1.id
        )
        teacher2 = add_user(
            'oliver keers',
            'keo@keo.com',
            'keerspass',
            TEACHER,
            'KEO',
            school2.id
        )
        teacher3 = add_user(
            'bobby',
            'bob@bob.com',
            'bobpass',
            TEACHER,
            'CUB',
            school2.id
        )

        tech = add_user(
            'gary tyler',
            'gary@gary.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school2.id
        )

        # teacher 2 and teacher 3 both from technician's
        # school, teacher 1 from other school

        add_req(
            "title1",
            "equipment",
            "notes",
            datetime.now(),
            teacher1.id,
            school1.id
        )
        add_req(
            "title2",
            "equipment2",
            "notes2",
            datetime.now(),
            teacher1.id,
            school1.id
        )

        add_req(
            "title3",
            "equipment3",
            "notes3",
            datetime.now(),
            teacher2.id,
            school2.id
        )
        add_req(
            "title4",
            "equipment4",
            "notes4",
            datetime.now(),
            teacher2.id,
            school2.id
        )

        add_req(
            "title5",
            "equipment5",
            "notes5",
            datetime.now(),
            teacher3.id,
            school2.id
        )

        add_req(
            "title6",
            "equipment6",
            "notes6",
            datetime.now(),
            teacher3.id,
            school2.id
        )

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'gary@gary.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/reqs',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)

            for req in data['data']['reqs']:
                self.assertEqual(req['school_id'], tech.school_id)

            self.assertIn('success', data['status'])

    def test_query_older_reqs_returns_correct_reqs(self):

        """ensure get reqs with "older" query returns correct reqs"""

        req1date = datetime.now()
        req2date = req1date - timedelta(weeks=6)

        school1 = add_school(name='testschool')

        teacher1 = add_user(
            'ollie mansell', 'test@test.com', 'olliepass',
            TEACHER, 'MAO', school1.id)

        add_user(
            'gary tyler', 'gary@gary.com', 'garypass', TECHNICIAN,
            'TGA', school1.id)

        my_req = Req(
            title="title1",
            equipment="equipment1",
            notes="notes1",
            time=req1date,
            user_id=teacher1.id,
            school_id=school1.id,
            lesson_id=1)

        my_req2 = Req(
            title="title2",
            equipment="equipment2",
            notes="notes2",
            time=req2date,
            user_id=teacher1.id,
            school_id=school1.id,
            lesson_id=1)
        db.session.add(my_req)
        db.session.add(my_req2)
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'gary@gary.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/reqs?older=1',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['reqs']), 1)
            self.assertIn('title2', data['data']['reqs'][0]['title'])

    def test_get_without_date_query_doesnt_return_old_reqs(self):

        """ensure no date query only gets reqs less than 2 weeks old"""

        school1 = add_school(name='testschool')
        teacher1 = add_user(
            'ollie mansell', 'test@test.com', 'olliepass',
            TEACHER, 'MAO', school1.id)

        add_user(
            'gary tyler', 'gary@gary.com', 'garypass',
            TECHNICIAN, 'TGA', school1.id)

        add_req(
            "title1", "equipment1", "notes1", datetime.now(),
            teacher1.id, school1.id)

        add_req(
            "title2", "equipment2", "notes2",
            datetime.now() - timedelta(weeks=6), teacher1.id, school1.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'gary@gary.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/reqs',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            print("Length of reqs data object: {}".format(
                len(data['data']['reqs'])))
            self.assertEqual(len(data['data']['reqs']), 1)
            self.assertIn('title1', data['data']['reqs'][0]['title'])

    def test_get_schools_reqs_as_technician_discount_old_reqs(self):
        """ensure get /reqs as technician returns
        that schools reqs less than 2 weeks old"""

        school1 = add_school(name='testschool')
        school2 = add_school(name='testschool2')

        now = datetime.now()

        teacher1 = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school1.id)

        teacher2 = add_user(
            'oliver keers',
            'keo@keo.com',
            'keerspass',
            TEACHER,
            'KEO',
            school2.id)
        teacher3 = add_user(
            'bobby',
            'bob@bob.com',
            'bobpass',
            TEACHER,
            'CUB',
            school2.id)

        add_user(
            'gary tyler',
            'gary@gary.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school2.id)

        # other_req
        add_req(
            "teacher 1 school 1 current",
            "equipment",
            "notes",
            now,
            teacher1.id,
            school1.id)

        # other_req2
        add_req(
            "teach 1 school 1 old",
            "equipment2",
            "notes2", now - timedelta(weeks=6),
            teacher1.id,
            school1.id)

        add_req(
            "SHOULD RETURN",
            "equipment3",
            "notes3",
            now,
            teacher2.id,
            school2.id)

        add_req(
            "SHOULD RETURN",
            "equipment5",
            "notes5",
            now,
            teacher3.id,
            school2.id)

        add_req(
            "teach 2 school 2 old",
            "equipment4",
            "notes4",
            now - timedelta(weeks=6),
            teacher2.id,
            school2.id)

        add_req(
            "teach 3 school 2 old",
            "equipment6",
            "notes6",
            now - timedelta(weeks=6),
            teacher3.id,
            school2.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'gary@gary.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.get(
                '/reqs',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)

            for req in data['data']['reqs']:
                self.assertEqual(req['title'], "SHOULD RETURN")

            self.assertIn('success', data['status'])

    def test_time_survives_trip_to_dict_and_back(self):
        school1 = add_school(name='testschool')
        teacher1 = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school1.id)
        my_req = add_req(
            "title1",
            "equipment1",
            "notes1",
            datetime.now(),
            teacher1.id,
            school1.id)

        self.assertTrue(isinstance(my_req.time, datetime))

        my_req_d = my_req.asdict(exclude_pk=True)

        my_req_d['title'] = 'new title'

        my_req.fromdict(my_req_d)

        self.assertTrue(isinstance(my_req.time, datetime))

    def test_delete_req_by_teacher(self):

        """ensure correct response if req is deleted by a teacher"""

        school = add_school(name='testschool')
        teacher = add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher.id,
            school.id)
        req_id_retain = req.id

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.delete(
                '/reqs/' + str(req.id),
                headers={'Authorization': f'Bearer {token}'}
            )

            req = Req.query.get(req_id_retain)
            self.assertTrue(req is None)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                'Req {} has been deleted.'.format(req_id_retain),
                data['message'])
            self.assertIn('success', data['status'])

    def test_delete_req_by_teacher_not_own_req(self):

        """ensure correct response if req is deleted by a teacher"""

        school = add_school(name='testschool')
        add_user(
            'ollie mansell',
            'test@test.com',
            'olliepass',
            TEACHER,
            'MAO',
            school.id)
        teacher2 = add_user(
            'ollie keers',
            'keo@test.com',
            'keopass',
            TEACHER,
            'MAO',
            school.id)

        add_user(
            'gary tyler',
            'test2@test.com',
            'garypass',
            TECHNICIAN,
            'TGA',
            school.id)

        now = datetime.now()
        req = add_req(
            "title", "equipment", "notes",
            now, teacher2.id, school.id)
        req_id_retain = req.id
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.delete(
                '/reqs/' + str(req.id),
                headers={'Authorization': f'Bearer {token}'}
            )

            req = Req.query.get(req_id_retain)
            self.assertTrue(req is not None)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You are not authorised to do that.',
                data['message'])
            self.assertIn('fail', data['status'])

    def test_delete_req_by_technician(self):

        """ensure correct response if req is deleted by a technician"""

        school = add_school(name='testschool')

        add_user(
            'ollie mansell', 'test@test.com',
            'olliepass', TEACHER, 'MAO', school.id)
        teacher2 = add_user(
            'ollie keers', 'keo@test.com', 'keopass',
            TEACHER, 'MAO', school.id)

        add_user(
            'gary tyler', 'test2@test.com', 'garypass',
            TECHNICIAN, 'TGA', school.id)

        now = datetime.now()
        req = add_req(
            "title",
            "equipment",
            "notes",
            now,
            teacher2.id,
            school.id)

        req_id_retain = req.id

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test2@test.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.delete(
                '/reqs/' + str(req.id),
                headers={'Authorization': f'Bearer {token}'}
            )

            req = Req.query.get(req_id_retain)
            self.assertTrue(req is None)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                'Req {} has been deleted.'.format(req_id_retain),
                data['message'])
            self.assertIn('success', data['status'])

    def test_delete_req_doesnt_exist(self):

        """ensure correct response if non-existant req is deleted."""

        school = add_school(name='testschool')
        add_user(
            'ollie mansell', 'test@test.com', 'olliepass',
            TEACHER, 'MAO', school.id)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.delete(
                '/reqs/100',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Req does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_delete_req_wrong_school(self):

        """ensure correct response if req is
            deleted by staff from wrong school"""

        school = add_school(name='testschool')
        school2 = add_school(name='testschool2')
        add_user(
            'ollie mansell', 'test@test.com', 'olliepass',
            TEACHER, 'MAO', school.id)
        teacher2 = add_user(
            'ollie keers', 'keo@test.com', 'keopass', TEACHER,
            'MAO', school2.id)

        now = datetime.now()
        req = add_req(
            "title", "equipment", "notes", now,
            teacher2.id, school2.id)

        req_id_retain = req.id

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.delete(
                '/reqs/' + str(req.id),
                headers={'Authorization': f'Bearer {token}'}
            )

            req = Req.query.get(req_id_retain)
            self.assertTrue(req is not None)

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'You are not authorised to do that.', data['message'])
            self.assertIn('fail', data['status'])
