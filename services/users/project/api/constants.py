from collections import OrderedDict, namedtuple

AUTUMN1 = 0
AUTUMN2 = 1
SPRING1 = 2
SPRING2 = 3
SUMMER1 = 4
SUMMER2 = 5
START = 0
END = 1


TEACHER = 1
TECHNICIAN = 2
USER_ROLE = {
    TEACHER: 'teacher',
    TECHNICIAN: 'technician'
}
USER_ROLE = OrderedDict(sorted(USER_ROLE.items()))

TEACHER_PATCH_AUTH = ['title', 'equipment', 'notes']
TECHNICIAN_PATCH_AUTH = ['isDone', 'hasIssue', 'issue_text']

HalfTerm = namedtuple('HalfTerm', ['start', 'end'])

PREFERENCES_TEMPLATE = {
    "dates_processed": False,
    "days_notice": 7,
    "term_dates": [
            HalfTerm('null', 'null'),
            HalfTerm('null', 'null'),
            HalfTerm('null', 'null'),
            HalfTerm('null', 'null'),
            HalfTerm('null', 'null'),
            HalfTerm('null', 'null')
        ],
    "week_number_start": [],
    "period_start_times": {},
    "period_length_in_minutes": 60,
    "weeks_timetable": 1,
    "sites": False,
    "reminder_emails": False,
    "reminder_day": 3,  # ISO WEEKDAY
}

HIDDEN_PREFERENCES = ['dates_processed']

EDITABLE_PREFERENCES = ['/'+key for key in PREFERENCES_TEMPLATE
                        if key not in HIDDEN_PREFERENCES]

DAY_TO_ISO = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5}

DATE_FORMAT = "%Y%m%d"
DATETIME_FORMAT = "%Y%m%dT%H%M"
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S"
TIME_FORMAT = "%H%M"
POSTGRES_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
