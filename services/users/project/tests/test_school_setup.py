import json

from project import db
from project.api.models import User, School

from project.tests.base import BaseTestCase
from project.tests.utils import add_school
from project.api.constants import TEACHER, TECHNICIAN, ADMIN, HalfTerm

import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestSchoolSetup(BaseTestCase):

    def test_create_school(self):

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO'
        )
        db.session.add(user)

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
                '/schools',
                data=json.dumps({
                    'name': 'testschool2',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            s = School.query.filter_by(name='testschool2').first()

            self.assertEqual(response.status_code, 201)
            self.assertIn('testschool2 has been created.', data['message'])
            self.assertEqual(s.id, user.school_id)
            self.assertIn('success', data['status'])
            self.assertIn('testschool2', data['data']['name'])

    def test_create_school_teacher(self):
        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            staff_code='MAO'
        )
        db.session.add(user)

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
                '/schools',
                data=json.dumps({
                    'name': 'testschool2',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )

            s = School.query.filter_by(name='testschool2').first()

            self.assertTrue(s is None)

            self.assertEqual(response.status_code, 401)
            # self.assertIn('testschool2 has been created.', data['message'])
            # self.assertEqual(s.id, user.school_id)
            # self.assertIn('success', data['status'])
            # self.assertIn('testschool2', data['data']['name'])

    def test_create_school_technician(self):
        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TECHNICIAN,
            staff_code='MAO'
        )
        db.session.add(user)

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
                '/schools',
                data=json.dumps({
                    'name': 'testschool2',
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            s = School.query.filter_by(name='testschool2').first()

            self.assertTrue(s is None)

            self.assertEqual(response.status_code, 401)
            # self.assertIn('testschool2 has been created.', data['message'])
            # self.assertEqual(s.id, user.school_id)
            # self.assertIn('success', data['status'])
            # self.assertIn('testschool2', data['data']['name'])

    def test_create_school_invalid_JSON(self):
        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO'
        )
        db.session.add(user)
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
                '/schools',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid payload.', data['message'])

    def test_patch_school_with_preferences_update(self):

        school = add_school('Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps([{
                    "op": "replace",
                    "path": "/days_notice", "value": 3
                    },
                    {
                    "op": "replace",
                    "path": "/reminder_emails", "value": True
                    },
                    {
                    "op": "replace",
                    "path": "/weeks_timetable", "value": 2
                    },
                    {
                    "op": "replace",
                    "path": "/term_dates", "value":
                    [
                        HalfTerm("01-09-17", "20-10-17"),
                        HalfTerm("30-10-17", "20-12-17"),
                        HalfTerm("03-01-18", "09-02-18"),
                        HalfTerm("19-02-18", "29-03-18"),
                        HalfTerm("16-04-18", "25-05-18"),
                        HalfTerm("04-06-18", "20-07-18")
                    ],
                    },
                    {
                        "op": "replace",
                        "path": "/period_start_times", "value":
                        {'1': '0900',
                            '2': '1000',
                            '3': '1120',
                            '4': '1220',
                            '5': '1410',
                            '6': '1510'}
                    }
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertIn(
                "Preferences for {} have been updated.".format(school.name),
                data['message'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(school.preferences['reminder_emails'], True)
            self.assertEqual(school.preferences['days_notice'], 3)
            self.assertEqual(school.preferences['weeks_timetable'], 2)
            self.assertEqual(
                school.preferences['term_dates'][0][0],
                "01-09-17")
            self.assertEqual(
                school.preferences['term_dates'][5][1], "20-07-18")

            self.assertIn("success", data['status'])
            self.assertIn(
                "Holy Family Catholic School", data['data']['school']['name']
            )

    def test_patch_school_with_preferences_update_teacher_fails(self):

        school = add_school('Trinity College')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps([{
                    "op": "replace",
                    "path": "/days_notice", "value": 6
                    },
                    {
                    "op": "replace",
                    "path": "/reminder_emails", "value": True
                    },
                    {
                    "op": "replace",
                    "path": "/weeks_timetable", "value": 1
                    },
                    {
                    "op": "replace",
                    "path": "/term_dates", "value":
                        [
                            HalfTerm("01-09-17", "20-10-17"),
                            HalfTerm("30-10-17", "20-12-17"),
                            HalfTerm("03-01-18", "09-02-18"),
                            HalfTerm("19-02-18", "29-03-18"),
                            HalfTerm("16-04-18", "25-05-18"),
                            HalfTerm("04-06-18", "20-07-18")
                        ]
                    }
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertIn(
                "You must be admin to do that.",
                data['message'])
            self.assertEqual(response.status_code, 401)
            self.assertEqual(school.preferences['reminder_emails'], False)
            self.assertEqual(school.preferences['days_notice'], 7)
            self.assertEqual(school.preferences['weeks_timetable'], 1)
            self.assertEqual(
                school.preferences['term_dates'][0][0],
                'null')
            self.assertIn("fail", data['status'])

    def test_patch_school_with_preferences_update_technician_fails(self):

        school = School(
            name='Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TECHNICIAN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps([{
                    "op": "replace",
                    "path": "/days_notice", "value": 10
                    },
                    {
                    "op": "replace",
                    "path": "/reminder_emails", "value": True
                    },
                    {
                    "op": "replace",
                    "path": "/weeks_timetable", "value": 1
                    },
                    {
                    "op": "replace",
                    "path": "/term_dates", "value":
                        [
                            HalfTerm("01-09-17", "20-10-17"),
                            HalfTerm("30-10-17", "20-12-17"),
                            HalfTerm("03-01-18", "09-02-18"),
                            HalfTerm("19-02-18", "29-03-18"),
                            HalfTerm("16-04-18", "25-05-18"),
                            HalfTerm("04-06-18", "20-07-18")
                        ]
                    }
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertIn(
                "You must be admin to do that.",
                data['message'])
            self.assertEqual(response.status_code, 401)
            self.assertEqual(school.preferences['reminder_emails'], False)
            self.assertEqual(school.preferences['days_notice'], 7)
            self.assertEqual(school.preferences['weeks_timetable'], 1)
            self.assertEqual(
                school.preferences['term_dates'][0][0],
                'null')
            self.assertIn("fail", data['status'])

    def test_patch_preferences_invalid_JSON(self):
        school = add_school('Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps([{}]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertIn(
                'Malformed patch.',
                data['message'])
            self.assertEqual(response.status_code, 400)
            self.assertIn("fail", data['status'])

    def test_patch_preferences_wrong_patch_paths(self):
        school = add_school('Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps([{
                    "op": "replace",
                    "path": "/lala", "value": 3
                    },
                    {
                    "op": "replace",
                    "path": "/lalala", "value": True
                    },
                    {
                    "op": "replace",
                    "path": "/weeks_timetable", "value": 2
                    },
                    {
                    "op": "replace",
                    "path": "/term_dates", "value":
                        [
                            HalfTerm("01-09-17", "20-10-17"),
                            HalfTerm("30-10-17", "20-12-17"),
                            HalfTerm("03-01-18", "09-02-18"),
                            HalfTerm("19-02-18", "29-03-18"),
                            HalfTerm("16-04-18", "25-05-18"),
                            HalfTerm("04-06-18", "20-07-18")
                        ]
                    }
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertIn(
                "Malformed patch.".format(school.name),
                data['message'])
            self.assertEqual(response.status_code, 400)
            self.assertEqual(school.preferences['reminder_emails'], False)
            self.assertEqual(school.preferences['days_notice'], 7)
            self.assertEqual(school.preferences['weeks_timetable'], 1)
            self.assertEqual(
                school.preferences['term_dates'][0][0],
                'null')

            self.assertIn("fail", data['status'])

    def test_patch_preferences_malformed_dates(self):
        school = add_school('Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps([{
                    "op": "replace",
                    "path": "/days_notice", "value": 3
                    },
                    {
                    "op": "replace",
                    "path": "/reminder_emails", "value": True
                    },
                    {
                    "op": "replace",
                    "path": "/weeks_timetable", "value": 2
                    },
                    {
                    "op": "replace",
                    "path": "/term_dates", "value":
                        [
                            HalfTerm("01-09-2017", "20-10-17"),
                            HalfTerm("30-10-17", "20-12-17"),
                            HalfTerm("03-01-18", "09-02-18"),
                            HalfTerm("19-02-18", "29-03-18"),
                            HalfTerm("16-04-18", "25-05-18"),
                            HalfTerm("04-06-18", "20-07-18")
                        ]
                    }
                    ]),
                headers={'Authorization': f'Bearer {token}'}
            )

            data = json.loads(response.data.decode())

            self.assertIn(
                "Malformed patch.".format(school.name),
                data['message'])
            self.assertEqual(response.status_code, 400)
            self.assertEqual(school.preferences['reminder_emails'], False)
            self.assertEqual(school.preferences['days_notice'], 7)
            self.assertEqual(school.preferences['weeks_timetable'], 1)
            self.assertEqual(
                school.preferences['term_dates'][0][0],
                'null')

            self.assertIn("fail", data['status'])

    def test_update_period_times(self):

        school = add_school('Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps(
                    [
                        {
                            "op": "replace",
                            "path": "/period_start_times", "value":
                            {'1': '0900',
                                '2': '1000',
                                '3': '1120',
                                '4': '1220',
                                '5': '1410',
                                '6': '1510'}
                        },
                        {
                            "op": "replace",
                            "path": "/period_length_in_minutes",
                            "value": 60
                        },
                        {
                            "op": "replace",
                            "path": "/period_start_times", "value":
                            {'1': '0900',
                                '2': '1000',
                                '3': '1120',
                                '4': '1220',
                                '5': '1410',
                                '6': '1510'}
                        }
                    ]),
                headers={'Authorization': f'Bearer {token}'})

            data = json.loads(response.data.decode())

            self.assertIn(
                "Preferences for {} have been updated.".format(school.name),
                data['message'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(school.preferences['reminder_emails'], False)
            self.assertEqual(school.preferences['days_notice'], 7)
            self.assertEqual(school.preferences['weeks_timetable'], 1)
            self.assertEqual(
                school.preferences['period_start_times']['1'], '0900')
            self.assertEqual(
                school.preferences['period_start_times']['2'], '1000')
            self.assertEqual(
                school.preferences['period_length_in_minutes'], 60)
            # self.assertEqual(
            #     school.preferences['term_dates']['autm_h1_s'],
            #     start_of_term.strftime(DATE_FORMAT))

            self.assertIn("success", data['status'])

    def test_update_period_times_invalid_period_length(self):

        school = add_school('Holy Family Catholic School')

        user = User(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=ADMIN,
            staff_code='MAO',
            school_id=school.id
        )
        db.session.add(user)
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

            response = self.client.patch(
                '/schools/preferences',
                content_type='application/json',
                data=json.dumps(
                    [
                        {
                            "op": "replace",
                            "path": "/period_start_times", "value":
                            {'1': '0900',
                                '2': '1000',
                                '3': '1120',
                                '4': '1220',
                                '5': '1410',
                                '6': '1510'}
                        },
                        {
                            "op": "replace",
                            "path": "/period_length_in_minutes",
                            "value": "01:00"
                        }
                    ]),
                headers={'Authorization': f'Bearer {token}'})

            data = json.loads(response.data.decode())

            self.assertIn(
                "invalid literal",
                data['message'])
            self.assertEqual(response.status_code, 400)
            self.assertEqual(school.preferences['reminder_emails'], False)
            self.assertEqual(school.preferences['days_notice'], 7)
            self.assertEqual(school.preferences['weeks_timetable'], 1)
            self.assertEqual(
                school.preferences['period_start_times'], {})
            self.assertEqual(
                school.preferences['period_length_in_minutes'], 60)
            # self.assertEqual(
            #     school.preferences['term_dates']['autm_h1_s'],
            #     start_of_term.strftime(DATE_FORMAT))

            self.assertIn("fail", data['status'])

    def test_staff_populate_from_SIMS(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='o.mansell@holyfamily.watham.sch.uk',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )

            db.session.add(user)
            db.session.commit()

            with self.client:
                resp_login = self.client.post(
                    '/auth/login',
                    data=json.dumps({
                        'email': 'o.mansell@holyfamily.watham.sch.uk',
                        'password': 'olliepass'
                    }),
                    content_type='application/json'
                )
                token = json.loads(resp_login.data.decode())['auth_token']

                response = self.client.post(
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename": "project/api/staffinfo.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "Please ensure these users are correct.",
                    data['message'])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(data['data']['staff']), 15)
                # self.assertEqual(school.preferences['days_notice'], 7)
                # self.assertEqual(school.preferences['weeks_timetable'], 1)
                # self.assertEqual(
                #     school.preferences['period_start_times'], 'null')
                # self.assertEqual(
                #     school.preferences['period_length'], 'null')
                # self.assertEqual(
                #     school.preferences['term_dates']['autm_h1_s'],
                #     start_of_term.strftime(DATE_FORMAT))

                self.assertIn("success", data['status'])

    def test_staff_lesson_room_populate_from_SIMS_wrong_filename(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )
            db.session.add(user)
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
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename": "project/api/staffinfo1.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "fail",
                    data['status'])
                self.assertEqual(response.status_code, 401)

    def test_staff_lesson_room_populate_from_SIMS_bad_emails(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )
            db.session.add(user)
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
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename": "project/api/staffinfo_bad_emails.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "fail",
                    data['status'])
                self.assertIn(
                    "Emails are incorrect.",
                    data['message'])
                self.assertEqual(response.status_code, 401)

    def test_staff_lesson_room_populate_from_SIMS_missing_names(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )
            db.session.add(user)
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
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename": "project/api/staffinfo_missing_name.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "fail",
                    data['status'])
                self.assertIn(
                    'Names are missing from the uploaded file.',
                    data['message']
                )

                self.assertEqual(response.status_code, 401)

    def test_staff_lesson_room_populate_from_SIMS_missing_staff_code(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )
            db.session.add(user)
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
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename":
                            "project/api/staffinfo_missing_staff_code.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "fail",
                    data['status'])
                self.assertIn(
                    'Staff codes are missing from the uploaded file.',
                    data['message']
                )

                self.assertEqual(response.status_code, 401)

    def test_staff_lesson_room_populate_from_SIMS_edited_from_original(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )
            db.session.add(user)
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
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename":
                            "project/api/staffinfo_edited_from_template.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "fail",
                    data['status'])
                self.assertIn(
                    'Please ensure you use the template provided.',
                    data['message']
                )
                self.assertEqual(response.status_code, 401)

    def test_staff_populate_from_SIMS_with_extant_users(self):

            school = add_school('Holy Family Catholic School')

            user = User(
                name='ollie mansell',
                email='o.mansell@holyfamily.watham.sch.uk',
                password='olliepass',
                role_code=ADMIN,
                staff_code='MAO',
                school_id=school.id
            )

            user2 = User(
                name='denise baxter',
                email='d.baxter@holyfamily.watham.sch.uk',
                password='olliepass',
                role_code=TEACHER,
                staff_code='BAD',
                school_id=school.id
            )
            db.session.add(user)
            db.session.add(user2)
            db.session.commit()

            with self.client:
                resp_login = self.client.post(
                    '/auth/login',
                    data=json.dumps({
                        'email': 'o.mansell@holyfamily.watham.sch.uk',
                        'password': 'olliepass'
                    }),
                    content_type='application/json'
                )
                token = json.loads(resp_login.data.decode())['auth_token']

                response = self.client.post(
                    '/schools/' + str(school.id) + '/staff',
                    content_type='application/json',
                    data=json.dumps(
                        {"filename": "project/api/staffinfo.xlsx"}
                        ),
                    headers={'Authorization': f'Bearer {token}'})

                data = json.loads(response.data.decode())

                self.assertIn(
                    "Please ensure these users are correct.",
                    data['message'])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    len(data['warning']['skipped_users']), 2)
                self.assertIn(
                    'o.mansell@holyfamily.watham.sch.uk',
                    data['warning']['skipped_users'])
                self.assertIn(
                    'd.baxter@holyfamily.watham.sch.uk',
                    data['warning']['skipped_users'])

                self.assertEqual(response.status_code, 200)
                self.assertIn("success", data['status'])
