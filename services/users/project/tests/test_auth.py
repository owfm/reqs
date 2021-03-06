# services/users/project/tests/test_auth.py

import json

from flask import current_app

from project import db


from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_school
from project.api.constants import TEACHER
from project.tests.utils import populate_school_db, populate_school_with_reqs

from project.api.models import School

import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestAuthBlueprint(BaseTestCase):

    def test_user_registration(self):

        with self.client:

            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'test@test.com',
                    'name': 'justatest',
                    'password': '123456',
                    'role_code': TEACHER,
                    'staff_code': "MAO"
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['user']['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        school = add_school('testschool')
        add_user('name', 'test@test.com', 'test', 1, 'MAO', school.id)

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'name': 'michael',
                    'email': 'test@test.com',
                    'password': 'test',
                    'role_code': TEACHER,
                    'staff_code': "MAO",
                    'school_id': 1
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'That email is already taken.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_name(self):
        school = add_school('testschool')

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                    'role_code': TEACHER,
                    'staff_code': "MAO",
                    'school_id': school.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('No name provided.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        school = add_school('testschool')

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'name': 'justatest',
                    'password': '123456',
                    'role_code': TEACHER,
                    'staff_code': "MAO",
                    'school_id': school.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('No email provided.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        school = add_school('testschool')

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'name': 'justatest',
                    'email': 'test@test.com',
                    'role_code': TEACHER,
                    'staff_code': "MAO",
                    'school_id': school.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('No password provided.', data['message'])
            self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        school = add_school('testschool')

        with self.client:
            add_user('name', 'test@test.com', 'test', 1, 'MAO', school.id)
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['user']['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_registered_user_login_with_db(self):

        school = School(name='Holy Family Catholic School')
        db.session.add(school)
        db.session.commit()

        populate_school_db(school.id)

        populate_school_with_reqs(school.id)

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'o.keers@holyfamily.watham.sch.uk',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['user']['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)
