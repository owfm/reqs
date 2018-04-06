# services/users/project/tests/test_user_model.py

from project.tests.base import BaseTestCase
from project.tests.utils import add_req, add_school, add_user
from project.api.constants import TEACHER

from datetime import datetime


class TestReqModel(BaseTestCase):

    def test_add_req(self):

        now = datetime.now()
        school = add_school('testschool')
        user = add_user(
            'ollie',
            'olli@ollie.com',
            'testpass',
            TEACHER,
            'MAO',
            school.id)

        req = add_req(
            'testtitle',
            'testequip',
            'testnotes',
            now,
            user.id,
            school.id)
        self.assertTrue(req.id)
        self.assertEqual(req.title, 'testtitle')
        self.assertEqual(req.equipment, 'testequip')
        self.assertEqual(req.notes, 'testnotes')
        self.assertEqual(req.time, now)
        self.assertFalse(req.isDone)
        self.assertFalse(req.hasIssue)
        self.assertEqual(req.user_id, user.id)
        self.assertEqual(req.school_id, school.id)
