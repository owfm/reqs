from project.tests.base import BaseTestCase
from project.api.school_utils import convert_dates_strings_to_datetime,\
    check_term_dates_sequential, check_in_term, get_week_beginning_date,\
    process_preferences, ensure_term_dates_are_weekdays, get_week_number
from project.api.constants import HalfTerm, DATE_FORMAT, SUMMER1, SUMMER2,\
    START, END, AUTUMN1, AUTUMN2, SPRING1, SPRING2

from datetime import datetime

import pprint

pp = pprint.PrettyPrinter(indent=4)


PREFERENCES = {
    "dates_processed": False,
    "days_notice": 3,
    "term_dates": [
        HalfTerm("20170904", "20171020"),
        HalfTerm("20171030", "20171220"),
        HalfTerm("20180103", "20180209"),
        HalfTerm("20180219", "20180329"),
        HalfTerm("20180416", "20180525"),
        HalfTerm("20180604", "20180720")
    ],
    "week_number_start": [],
    "period_start_times": {
        "1": "0900",
        "2": "1000",
        "3": "1120",
        "4": "1220",
        "5": "1410",
        "6": "1510"
    },
    "period_length_in_minutes": 60,
    "weeks_timetable": 2,
    "sites": True,
    "reminder_emails": False,
    "reminder_day": 3,  # ISO WEEKDAY
}

PREFERENCES_WEEKEND_STARTS = {
    "dates_processed": False,
    "days_notice": 3,
    "term_dates": [

        HalfTerm("20170903", "20171020"),
        HalfTerm("20171030", "20171220"),
        HalfTerm("20180103", "20180209"),
        HalfTerm("20180219", "20180329"),
        HalfTerm("20180416", "20180525"),
        HalfTerm("20180604", "20180720")
    ],
    "week_number_start": [],
    "period_start_times": {
        "1": "0900",
        "2": "1000",
        "3": "1120",
        "4": "1220",
        "5": "1410",
        "6": "1510"
    },
    "period_length_in_minutes": 60,
    "weeks_timetable": 1,
    "sites": True,
    "reminder_emails": False,
    "reminder_day": 3,  # ISO WEEKDAY
}

PREFERENCES_DATES_WRONG_ORDER = {
    "dates_processed": False,
    "days_notice": 3,
    "term_dates": [
        HalfTerm("20171030", "20171220"),
        HalfTerm("20170901", "20171020"),
        HalfTerm("20180103", "20180209"),
        HalfTerm("20180219", "20180329"),
        HalfTerm("20180416", "20180525"),
        HalfTerm("20180604", "20180720")
    ],
    "week_number_start": [],
    "period_start_times": {
        "1": "0900",
        "2": "1000",
        "3": "1120",
        "4": "1220",
        "5": "1410",
        "6": "1510"
    },
    "period_length_in_minutes": 60,
    "weeks_timetable": 1,
    "sites": True,
    "reminder_emails": False,
    "reminder_day": 3,  # ISO WEEKDAY
}


class TestSchoolUtils(BaseTestCase):

    def test_convert_date_string_to_datetime(self):

        self.assertFalse(isinstance(PREFERENCES["term_dates"][0][0], datetime))

        converted_dates = convert_dates_strings_to_datetime(
            PREFERENCES["term_dates"])

        self.assertTrue(isinstance(converted_dates[0][0], datetime))

    def test_check_sequential_term_dates(self):

        converted_dates_correct = convert_dates_strings_to_datetime(
            PREFERENCES["term_dates"])
        converted_dates_wrong = convert_dates_strings_to_datetime(
            PREFERENCES_DATES_WRONG_ORDER["term_dates"])

        self.assertFalse(check_term_dates_sequential(converted_dates_wrong))
        self.assertTrue(check_term_dates_sequential(converted_dates_correct))

    def test_check_in_term(self):

        term_dates = convert_dates_strings_to_datetime(
            PREFERENCES["term_dates"])

        # autumn term 1
        check_in_term_resp = check_in_term("20170904", term_dates)
        self.assertTrue(check_in_term_resp[0])
        self.assertEqual(check_in_term_resp[1], 0)

        # in summer term 2
        check_in_term_resp = check_in_term("20180614", term_dates)
        self.assertTrue(check_in_term_resp[0])
        self.assertEqual(check_in_term_resp[1], 5)

        # aftr summer term
        in_term, term_index = check_in_term("20180721", term_dates)
        self.assertFalse(in_term)
        self.assertEqual(term_index, -1)

        with self.assertRaises(ValueError):
            check_in_term("blahblah", term_dates)

    def test_get_week_beginning_date(self):
        # THURSDAY
        test_date = get_week_beginning_date("20180322")
        test_date_string = datetime.strftime(test_date, DATE_FORMAT)
        self.assertEqual(test_date_string, "20180319")

        # SATURDAY
        test_date = get_week_beginning_date("20180324")
        test_date_string = datetime.strftime(test_date, DATE_FORMAT)
        self.assertEqual(test_date_string, "20180319")

        # SUNDAY
        test_date = get_week_beginning_date("20180325")
        test_date_string = datetime.strftime(test_date, DATE_FORMAT)
        self.assertEqual(test_date_string, "20180319")

    def test_process_preferences(self):

        process_preferences(PREFERENCES)

        self.assertTrue(PREFERENCES["dates_processed"])
        self.assertEqual(PREFERENCES["week_number_start"][AUTUMN1], 1)
        self.assertEqual(PREFERENCES["week_number_start"][AUTUMN2], 2)
        self.assertEqual(PREFERENCES["week_number_start"][SPRING1], 1)
        self.assertEqual(PREFERENCES["week_number_start"][SPRING2], 1)
        self.assertEqual(PREFERENCES["week_number_start"][SUMMER1], 1)
        self.assertEqual(PREFERENCES["week_number_start"][SUMMER2], 1)

    def test_ensure_term_dates_are_weekdays(self):

        converted_dates = convert_dates_strings_to_datetime(
            PREFERENCES_WEEKEND_STARTS["term_dates"])

        ensure_term_dates_are_weekdays(converted_dates)

        self.assertEqual(datetime.strftime(
            converted_dates[AUTUMN1][START], DATE_FORMAT), "20170904")
        self.assertEqual(datetime.strftime(
            converted_dates[AUTUMN1][END], DATE_FORMAT), "20171020")

    def test_get_week_number(self):

        process_preferences(PREFERENCES)

        test1 = datetime.strptime("20170905", DATE_FORMAT)
        self.assertEqual(get_week_number(test1, PREFERENCES), 1)

        test2 = datetime.strptime("20170911", DATE_FORMAT)
        self.assertEqual(get_week_number(test2, PREFERENCES), 2)

        test3 = datetime.strptime("20180425", DATE_FORMAT)
        self.assertEqual(get_week_number(test3, PREFERENCES), 2)
