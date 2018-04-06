# services/users/project/tests/test_user_model.py


from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_school
from project.api.constants import TEACHER


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        school = add_school('testschool')

        user = add_user(
            'justatest',
            'test@test.com',
            'test',
            TEACHER,
            'MAO',
            school.id)
        self.assertTrue(user.id)
        self.assertEqual(user.name, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertEqual(user.role_code, TEACHER)
        self.assertEqual(user.school_id, 1)

    def test_add_user_duplicate_email(self):
        school = add_school('testschool')

        add_user(
            'justatest',
            'test@test.com',
            'test',
            TEACHER,
            'MAO',
            school.id)

        duplicate_user = User(
                name='justatest',
                email='test@test.com',
                password='test',
                role_code=TEACHER,
                staff_code='MAO',
                school_id=school.id)
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    # def test_to_json(self):
    #     school = add_school('testschool')
    #
    #     user = add_user(
    #         'justatest',
    #         'test@test.com',
    #         'test',
    #         TEACHER,
    #         'MAO',
    #         school.id)
    #     self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        school = add_school('testschool')

        user_one = add_user(
            'justatest',
            'test@test2.com',
            'test',
            TEACHER,
            'MAO',
            school.id)
        user_two = add_user(
            'justatest',
            'test@test.com',
            'test',
            TEACHER,
            'MAO',
            school.id)
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        school = add_school('testschool')

        user = add_user(
            'justatest',
            'test@test.com',
            'test',
            TEACHER,
            'MAO',
            school.id)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        school = add_school('testschool')

        user = add_user(
            'justatest',
            'test@test.com',
            'test',
            TEACHER,
            'MAO',
            school.id)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token), user.id)
