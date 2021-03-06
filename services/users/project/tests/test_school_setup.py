import json

from project import db
from project.api.models import School

from project.tests.base import BaseTestCase
from project.tests.utils import add_school, add_user
from project.api.constants import TEACHER, TECHNICIAN, HalfTerm

import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestSchoolSetup(BaseTestCase):

    def test_create_school(self):

        user = add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            staff_code='MAO',
            admin=True
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

    def test_create_school_invalid_JSON(self):
        user = add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            staff_code='MAO',
            admin=True
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
            token = json.loads(resp_login.data.decode())['user']['token']

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

        user = add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            staff_code='MAO',
            admin=True,
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
                        HalfTerm("20170901", "20171020"),
                        HalfTerm("20171030", "20171220"),
                        HalfTerm("20180103", "20180209"),
                        HalfTerm("20180219", "20180329"),
                        HalfTerm("20180416", "20180525"),
                        HalfTerm("20180604", "20180720")
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
                "20170901")
            self.assertEqual(
                school.preferences['term_dates'][5][1], "20180720")

            self.assertIn("success", data['status'])
            self.assertIn(
                "Holy Family Catholic School", data['data']['school']['name']
            )

    def test_patch_school_with_preferences_update_teacher_fails(self):

        school = add_school('Trinity College')

        user = add_user(
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
                            HalfTerm("20170901", "20171020"),
                            HalfTerm("20171030", "20171220"),
                            HalfTerm("20180103", "20180209"),
                            HalfTerm("20180219", "20180329"),
                            HalfTerm("20180416", "20180525"),
                            HalfTerm("20180604", "20180720")
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

        user = add_user(
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
                            HalfTerm("20170901", "20171020"),
                            HalfTerm("20171030", "20171220"),
                            HalfTerm("20180103", "20180209"),
                            HalfTerm("20180219", "20180329"),
                            HalfTerm("20180416", "20180525"),
                            HalfTerm("20180604", "20180720")
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

        user = add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            admin=True,
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
            token = json.loads(resp_login.data.decode())['user']['token']

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

        user = add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            admin=True,
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
                            HalfTerm("20170901", "20171020"),
                            HalfTerm("20171030", "20171220"),
                            HalfTerm("20180103", "20180209"),
                            HalfTerm("20180219", "20180329"),
                            HalfTerm("20180416", "20180525"),
                            HalfTerm("20180604", "20180720")
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

        user = add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            admin=True,
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
            token = json.loads(resp_login.data.decode())['user']['token']

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
                            HalfTerm("170901", "20171020"),
                            HalfTerm("171030", "20171220"),
                            HalfTerm("180103", "20180209"),
                            HalfTerm("180219", "20180329"),
                            HalfTerm("180416", "20180525"),
                            HalfTerm("180604", "20180720")
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

        add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            admin=True,
            staff_code='MAO',
            school_id=school.id
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

        add_user(
            name='ollie mansell',
            email='test@test.com',
            password='olliepass',
            role_code=TEACHER,
            admin=True,
            staff_code='MAO',
            school_id=school.id
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

    def test_staff_lesson_room_populate_from_SIMS_wrong_filename(self):

            school = add_school('Holy Family Catholic School')

            add_user(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=TEACHER,
                admin=True,
                staff_code='MAO',
                school_id=school.id
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

            add_user(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=TEACHER,
                admin=True,
                staff_code='MAO',
                school_id=school.id
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

            add_user(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=TEACHER,
                admin=True,
                staff_code='MAO',
                school_id=school.id
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

            add_user(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=TEACHER,
                admin=True,
                staff_code='MAO',
                school_id=school.id
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

            add_user(
                name='ollie mansell',
                email='test@test.com',
                password='olliepass',
                role_code=TEACHER,
                admin=True,
                staff_code='MAO',
                school_id=school.id
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

            add_user(
                name='ollie mansell',
                email='o.mansell@holyfamily.watham.sch.uk',
                password='olliepass',
                role_code=TEACHER,
                admin=True,
                staff_code='MAO',
                school_id=school.id
            )

            add_user(
                name='denise baxter',
                email='d.baxter@holyfamily.watham.sch.uk',
                password='olliepass',
                role_code=TEACHER,
                staff_code='BAD',
                school_id=school.id
            )

            with self.client:
                resp_login = self.client.post(
                    '/auth/login',
                    data=json.dumps({
                        'email': 'o.mansell@holyfamily.watham.sch.uk',
                        'password': 'olliepass'
                    }),
                    content_type='application/json'
                )
                token = json.loads(resp_login.data.decode())['user']['token']

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
