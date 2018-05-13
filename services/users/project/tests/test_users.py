# services/users/project/tests/test_users.py

import json

from project import db
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_school, populate_school_db,\
    populate_school_with_reqs
from project.api.excel import extract_users
from project.api.constants import TEACHER
import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_get_users_works_correctly(self):

        school = add_school(name='Holy Family Catholic School')
        school2 = add_school(name='Trinity College')

        # admin1
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='o.mansell@holyfamily.watham.sch.uk', password='password',
            school_id=school.id, admin=True, role_code=TEACHER)
        # admin2
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='omansell@lgflmail.org', password='password',
            school_id=school2.id, admin=True, role_code=TEACHER)

        wb, staff = extract_users("project/api/staffinfo.xlsx")
        wb, staff2 = extract_users("project/api/staffinfo_school2.xlsx")

        for s in staff:
            if s['email'] == "o.mansell@holyfamily.watham.sch.uk":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school.id,
                password='password')
            db.session.add(new_user)

        for s in staff2:
            if s['email'] == "omansell@lgflmail.org":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school2.id,
                password='password')
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'o.mansell@holyfamily.watham.sch.uk',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/users',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            data = json.loads(response.data.decode())

            self.assertIn("success", data['status'])
            self.assertNotIn("holyfamily.waltham", data['data']['users'][1])
            self.assertEqual(15, len(data['data']['users']))
            self.assertEqual(response.status_code, 200)

    def test_get_users_as_teacher(self):

        school = add_school(name='Holy Family Catholic School')
        school2 = add_school(name='Trinity College')
        # admin1
        add_user(
            name='Oliver Mansell', staff_code='MAO', role_code=TEACHER,
            email='o.mansell@holyfamily.watham.sch.uk', password='password',
            school_id=school.id, admin=True)
        # admin2
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='omansell@lgflmail.org', password='password',
            school_id=school2.id, admin=True, role_code=TEACHER)

        wb, staff = extract_users("project/api/staffinfo.xlsx")
        wb, staff2 = extract_users("project/api/staffinfo_school2.xlsx")

        for s in staff:
            if s['email'] == "o.mansell@holyfamily.watham.sch.uk":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school.id,
                password='password')
            db.session.add(new_user)

        for s in staff2:
            if s['email'] == "omansell@lgflmail.org":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school2.id,
                password='password')
            db.session.add(new_user)
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'd.baxter@holyfamily.watham.sch.uk',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/users',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            data = json.loads(response.data.decode())

            self.assertIn("fail", data['status'])
            self.assertIn("You must be admin to do that.", data['message'])
            self.assertEqual(response.status_code, 401)

    def test_get_users_as_technician(self):

        school = add_school(name='Holy Family Catholic School')
        school2 = add_school(name='Trinity College')
        # admin1
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='o.mansell@holyfamily.watham.sch.uk', password='password',
            school_id=school.id, admin=True, role_code=TEACHER)
        # admin2
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='omansell@lgflmail.org', password='password',
            school_id=school2.id, admin=True, role_code=TEACHER)

        wb, staff = extract_users("project/api/staffinfo.xlsx")
        wb, staff2 = extract_users("project/api/staffinfo_school2.xlsx")

        for s in staff:
            if s['email'] == "o.mansell@holyfamily.watham.sch.uk":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school.id,
                password='password')

        for s in staff2:
            if s['email'] == "omansell@lgflmail.org":
                continue

            add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school2.id,
                password='password')
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 's.mannion@holyfamily.watham.sch.uk',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/users',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            data = json.loads(response.data.decode())

            self.assertIn("fail", data['status'])
            self.assertIn("You must be admin to do that.", data['message'])
            self.assertEqual(response.status_code, 401)

    def test_get_self(self):

        school = add_school(name='Holy Family Catholic School')
        school2 = add_school(name='Trinity College')
        # admin1
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='o.mansell@holyfamily.watham.sch.uk', password='password',
            school_id=school.id, admin=True, role_code=TEACHER)
        # admin2
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='omansell@lgflmail.org', password='password',
            school_id=school2.id, admin=True, role_code=TEACHER)

        wb, staff = extract_users("project/api/staffinfo.xlsx")
        wb, staff2 = extract_users("project/api/staffinfo_school2.xlsx")

        for s in staff:
            if s['email'] == "o.mansell@holyfamily.watham.sch.uk":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school.id,
                password='password')
            db.session.add(new_user)

        for s in staff2:
            if s['email'] == "omansell@lgflmail.org":
                continue

            new_user = add_user(
                name=s['name'], email=s['email'], role_code=s['role_code'],
                staff_code=s['staff_code'], school_id=school2.id,
                password='password')
            db.session.add(new_user)
        db.session.commit()

        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'i.mensah@holyfamily.watham.sch.uk',
                    'password': 'password'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['user']['token']

            response = self.client.get(
                '/users/me',
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            data = json.loads(response.data.decode())

            self.assertIn("success", data['status'])
            self.assertIn("Isaac", data['data']['name'])
            self.assertEqual(response.status_code, 200)

    def test_populate_db_function(self):
        school = add_school(name='Holy Family Catholic School')
        # admin
        add_user(
            name='Oliver Mansell', staff_code='MAO',
            email='o.mansell@holyfamily.watham.sch.uk', password='password',
            school_id=school.id, admin=True, role_code=TEACHER)

        populate_school_db(school.id)

        populate_school_with_reqs(school.id)
