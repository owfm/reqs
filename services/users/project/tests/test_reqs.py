import json

from datetime import datetime, timedelta

from project import db
from project.api.models import Req, User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_req, add_school
from project.api.constants import TEACHER, TECHNICIAN, DATE_FORMAT

import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestReqService(BaseTestCase):

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
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'lesson_id': 1,
                    'currentWbStamp': '20180416'
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

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'olliepass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'lesson_id': 1,
                    'currentWbStamp': '20180416'
                    }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'You must provide a title for your requisition.',
                data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_has_correct_user_and_school_id(self):
        """Ensure a new req gets correct user_id from auth token."""

        school = add_school('testschool')

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
            token = json.loads(resp_login.data.decode())['user']['token']
            resp = User.decode_auth_token(token)

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'lesson_id': 1,
                    'currentWbStamp': '20180416'
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
                    'lesson_id': 1,
                    'currentWbStamp': '20180416'
                    }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Provide a valid auth token.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_not_logged_in(self):
        """ensure can't post req without being logged in"""

        with self.client:
            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'lesson_id': 1,
                    'currentWbStamp': '20180416'
                    }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Provide a valid auth token.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_req_technician(self):
        """ ensure can't post req as technician"""

        school = add_school('testschool')

        add_user(
            'ollie mansell', 'test@test.com', 'olliepass',
            TECHNICIAN, 'MAO', school.id)

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
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.post(
                '/reqs',
                data=json.dumps({
                    'title': 'reqtitletest',
                    'equipment': 'equipmenttest',
                    'notes': 'notestest',
                    'lesson_id': 1,
                    'currentWbStamp': '20180416'
                    }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'As a technician you cannot submit requisitions.',
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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

        from_str = datetime.now().strftime(DATE_FORMAT)
        to_str = (datetime.now() + timedelta(days=10)).strftime(DATE_FORMAT)

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
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/reqs?wb=' + from_str,
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']), 2)

            for req in data['data']:
                self.assertEqual(req['user_id'], teacher.id)

            self.assertIn('success', data['status'])

    def test_get_schools_reqs_as_technician(self):
        """ensure get /reqs as technician returns that schools reqs only"""

        school1 = add_school(name='testschool1')
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

        tech = add_user(
            'Gary',
            'gary@gary.com',
            'garypass',
            TECHNICIAN,
            'GAY',
            school1.id
        )

        now = datetime.now() + timedelta(days=5)

        from_str = datetime.now().strftime(DATE_FORMAT)
        to_str = (datetime.now() + timedelta(days=10)).strftime(DATE_FORMAT)

        add_req(
            "title1",
            "equipment",
            "notes",
            now,
            teacher1.id,
            school1.id)

        add_req(
            "title2",
            "equipment2",
            "notes2",
            now,
            teacher1.id,
            school1.id
        )

        add_req(
            "title3",
            "equipment3",
            "notes3",
            now,
            teacher2.id,
            school2.id
        )
        add_req(
            "title4",
            "equipment4",
            "notes4",
            now,
            teacher2.id,
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
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/reqs?wb=' + from_str,
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']), 2)

            for req in data['data']:
                self.assertEqual(req['school_id'], tech.school_id)

            self.assertIn('success', data['status'])

    def test_req_date_query(self):

        school1 = add_school(name='testschool')
        school2 = add_school(name='testschool2')

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
            datetime(2018, 5, 27, 23, 59),
            teacher1.id,
            school1.id)

        # other_req2
        add_req(
            "SHOULD RETURN",
            "equipment3",
            "notes3",
            datetime(2018, 5, 21, 9, 0, 0),
            teacher2.id,
            school2.id)

        add_req(
            "SHOULD RETURN",
            "equipment3",
            "notes3",
            datetime(2018, 5, 21, 9, 0, 0),
            teacher2.id,
            school2.id)

        add_req(
            "SHOULD RETURN",
            "equipment5",
            "notes5",
            datetime(2018, 5, 25, 15, 10),
            teacher3.id,
            school2.id)

        add_req(
            "OLD REQ",
            "equipment6",
            "notes6",
            datetime(2018, 5, 18, 9, 0, 0),
            teacher3.id,
            school2.id)

        wb = datetime(2018, 5, 21).strftime(DATE_FORMAT)

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'gary@gary.com',
                    'password': 'garypass'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/reqs?wb=' + wb,
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)

            for req in data['data']:
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
            token = json.loads(resp_login.data.decode())['user']['token']

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
