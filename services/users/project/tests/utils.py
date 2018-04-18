# services/users/project/tests/utils.py

from project import db
from project.api.models import User, Req, School, Room, Classgroup, Lesson,\
    Site
from project.api.excel import extract_users, extract_lessons
from project.api.constants import TEACHER, TECHNICIAN, DATETIME_FORMAT,\
    TIME_FORMAT, HalfTerm
from project.api.school_utils import process_preferences
import pprint
from datetime import datetime, timedelta
import calendar
import random


nouns = ("test-tube", "leaves", "microscopes", "trolley", "phosphorus")
verbs = ("runs", "hits", "jumps", "drives", "barfs")
adv = ("gentle", "dutifully", "foolishly", "merrily", "fully")
adj = ("hot", "cold", "reactive", "several", "many")

words_type_list = [nouns, verbs, adj]


def gs(sentences):
    if sentences is 1:
        return ' '.join([random.choice(i) for i in words_type_list]) + '.'
    else:
        st = ''
        for i in range(sentences):
            st += ' '.join([random.choice(i) for i in words_type_list]) + '. '
        return st


pp = pprint.PrettyPrinter(indent=4)


def populate_school_with_reqs(school_id, number_to_create=50):

    """ creates a random req. Picks a random week in the next year and
    creates a random req in that week at the appropriate time. """

    school = School.query.get(school_id)

    technician_id_list = [user.id for user in User.query.filter_by(
        school_id=school_id).filter_by(role_code=TECHNICIAN).all()]
    lesson_id_list = [lesson.id for lesson in Lesson.query.filter_by(
        school_id=school_id).all()]

    for lesson in lesson_id_list:
        # grab random lesson
        lesson = Lesson.query.get(lesson)

        # grab random teacher
        teacher = User.query.get(lesson.teacher_id)

        # datetime format
        lesson_time = lesson.start_time

        # pick random week in the next 52 weeks:
        rand_52 = random.randrange(21)
        day_in_past_three_months = datetime.today() + \
            timedelta(weeks=1) - timedelta(days=rand_52)

        day_in_past_same_weekday_as_lesson = day_in_past_three_months + \
            timedelta(days=(
                lesson.day_code - day_in_past_three_months.isoweekday()))

        lesson_datetime = datetime.combine(
            day_in_past_same_weekday_as_lesson.date(), lesson_time)

        title = gs(1)
        equipment = gs(5)
        notes = gs(5)

        # create new req
        req = Req(
            title=title,
            equipment=equipment,
            notes=notes,
            time=lesson_datetime,
            user_id=teacher.id,
            school_id=school.id)

        req.lesson = lesson
        req.user = teacher
        req.school = school

        dice = random.random()

        if dice < 0.33:
            req.hasIssue = True
            req.issue_text = gs(2)
            req.issue_technician_id = technician_id_list[random.randrange(
                len(technician_id_list))]
        elif dice > 0.66:
            req.isDone = True
            req.done_by_id = technician_id_list[random.randrange(
                len(technician_id_list))]

        db.session.add(req)

    db.session.commit()


def lesson_to_JSON(lesson):

    # if not isinstance(monday_date, datetime):
    #     raise ValueError('Date passed is not a datetime object.')
    #
    # if monday_date.isoweekday() is not 1:
    #     raise ValueError('Date passed is not a Monday.')

    # TODO:  this should include some check of whether its the correct week'''

    lessonJSON = lesson.asdict(exclude=[
        'school_id', 'lesson_id', 'user_id', 'start_time', 'end_time',
        'day_code', 'week_number'])
    lessonJSON['type'] = 'lesson'

    lessonJSON['room'] = lesson.room.asdict(
        exclude_pk=True, exclude=["school_id"], follow=['site'])
    lessonJSON['classgroup'] = lesson.classgroup.asdict(
        exclude_pk=True, exclude=['school_id'])
    lessonJSON['teacher'] = lesson.teacher.asdict(
        exclude=['id', 'password', 'active', 'school_id'])

    # lesson_date = monday_date.date() + timedelta(days=lesson.day_code-1)
    # lessonJSON['time'] = lesson.start_time.strftime(TIME_FORMAT)
    lessonJSON['week'] = lesson.week_number
    lessonJSON['day'] = calendar.day_abbr[lesson.day_code - 1]

    return lessonJSON


def req_to_JSON(req):

    reqJSON = req.asdict()
    reqJSON['type'] = 'requisition'
    reqJSON['room'] = req.lesson.room.asdict(
        exclude_pk=True, exclude=["school_id"], follow=['site'])
    reqJSON['classgroup'] = req.lesson.classgroup.asdict(
        exclude_pk=True, exclude=['school_id'])
    reqJSON['teacher'] = req.user.asdict(
        exclude=['id', 'password', 'active', 'school_id'])
    reqJSON['day'] = calendar.day_abbr[req.lesson.day_code - 1]
    reqJSON['week'] = req.lesson.week_number
    reqJSON['period'] = req.lesson.period
    try:
        reqJSON['done_by'] = req.done_by.asdict(
            exclude=['id', 'password', 'active', 'school_id'])
    except AttributeError:
        pass
    try:
        reqJSON['issue_technician'] = req.issue_technician.asdict(
            exclude=['id', 'password', 'active', 'school_id'])
    except AttributeError:
        pass

    reqJSON['time'] = reqJSON['time'].strftime(DATETIME_FORMAT)
    reqJSON['submitted_at'] = reqJSON['submitted_at'].strftime(DATETIME_FORMAT)
    return reqJSON


def populate_school_db(
    school_id, reqs_number=150,
    lessons_file='project/api/SciTT2017.xlsx',
        staff_file="project/api/staffinfo.xlsx"):

    school = School.query.get(school_id)

    site1 = Site()
    site1.name = 'Wiseman Upstairs'
    site1.school_id = school.id
    db.session.add(site1)

    site3 = Site()
    site3.name = 'Wiseman Downstairs'
    site3.school_id = school.id
    db.session.add(site3)

    site2 = Site()
    site2.name = 'Walthamstow'
    site2.school_id = school.id
    db.session.add(site2)
    db.session.commit()

    if not school:
        return False

    lessons = extract_lessons(lessons_file)
    wb, staff = extract_users(staff_file)

    taken_emails = [u.email for u in User.query.filter_by(
        school_id=school_id).all()]

    for s in staff:
        if s['email'] in taken_emails:
            continue

        new_user = User(
            name=s['name'], email=s['email'], role_code=s['role_code'],
            staff_code=s['staff_code'], school_id=school.id,
            password='password')
        db.session.add(new_user)

    q = User.query.filter_by(
        email="o.mansell@holyfamily.watham.sch.uk").first()
    q.role_code = TEACHER
    db.session.commit()

    school.preferences = {
        "dates_processed": False,
        "days_notice": 7,
        "term_dates": [
                HalfTerm("01-09-17", "20-10-17"),
                HalfTerm("30-10-17", "20-12-17"),
                HalfTerm("03-01-18", "09-02-18"),
                HalfTerm("19-02-18", "29-03-18"),
                HalfTerm("16-04-18", "25-05-18"),
                HalfTerm("04-06-18", "20-07-18")
            ],
        "period_start_times": {
                            '1': '0900',
                            '2': '1000',
                            '3': '1120',
                            '4': '1220',
                            '5': '1410',
                            '6': '1510'
                            },
        "period_length_in_minutes": 60,
        "weeks_timetable": 2,
        "sites": True,
        "reminder_emails": False,
        "reminder_day": 3,  # ISO WEEKDAY
    }
    try:
        process_preferences(school.preferences)
    except ValueError:
        raise ValueError("Could not process preferences")

    for lesson in lessons:

        # rudimentary error checking that what should be numbers are numbers
        try:
            int(lesson['day'])
            int(lesson['period'])
            int(lesson['week'])
        except ValueError:
            continue

        teacher = User.query.filter_by(school_id=school_id).\
            filter_by(staff_code=lesson['staff_code']).first()

        if not teacher:
            return False

        room = Room.query.filter_by(school_id=school_id).\
            filter_by(name=lesson['room']).first()
        classgroup = Classgroup.query.filter_by(school_id=school_id).\
            filter_by(name=lesson['class']).first()

        if not room:

            room = Room(name=lesson['room'], school_id=school_id)

            if lesson['room'][0] is 'L':
                print("Room {} assigned Walthamstow".format(lesson['room']))
                room.site = Site.query.filter_by(
                    name='Walthamstow').first()
            elif int(lesson['room'][1] + lesson['room'][2]) < 18:
                print(
                    "Room {} assigned Wiseman "
                    "Downstairs".format(lesson['room']))

                room.site = Site.query.filter_by(
                    name='Wiseman Downstairs').first()
            else:
                print(
                    "Room {} assigned Wiseman "
                    "Upstairs".format(lesson['room']))

                room.site = Site.query.filter_by(
                    name='Wiseman Upstairs').first()

            room.site_id = random.randrange(1, 4)

            db.session.add(room)
            db.session.flush()
        if not classgroup:
            classgroup = Classgroup(
                name=lesson['class'],
                school_id=school_id)
            db.session.add(classgroup)
            db.session.flush()

        start_time = datetime.strptime(
            school.preferences['period_start_times'][str(lesson['period'])],
            TIME_FORMAT)

        end_time = start_time + timedelta(
            minutes=int(school.preferences['period_length_in_minutes']))

        lesson = Lesson(
            room=room, classgroup=classgroup, school=school,
            period=lesson['period'], week_number=lesson['week'],
            teacher=teacher, start_time=start_time,
            end_time=end_time, day_code=int(lesson['day']))

        db.session.add(lesson)
        db.session.flush()

    """should now have all teachers, lessons, and rooms in DB """
    db.session.commit()


def add_user(name, email, password, role_code, staff_code, school_id):
    user = User(name=name,
                email=email,
                password=password,
                role_code=role_code,
                staff_code=staff_code,
                school_id=school_id)
    db.session.add(user)
    db.session.commit()
    return user


def add_school(name):
    s = School(name=name)
    db.session.add(s)

    teacher_email = "teach@" + name + ".com"

    teacher = add_user(
        'Teachy Man', teacher_email, 'password', TEACHER, 'TEA', s.id)
    db.session.add(teacher)

    room1 = Room(name='Room', school_id=s.id)
    db.session.add(room1)

    classgroup1 = Classgroup(name='11b/Sc1', school_id=s.id)
    db.session.add(classgroup1)

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    start_time = start_time.time()
    end_time = end_time.time()

    lesson1 = Lesson(
        classgroup=classgroup1,
        room=room1,
        school=s,
        teacher=teacher,
        day_code=1,
        start_time=start_time,
        end_time=end_time
        )
    db.session.add(lesson1)

    db.session.commit()
    return s


def add_req(title, equipment, notes, time, user_id, school_id, lesson_id=1):

    req = Req(
            title=title,
            equipment=equipment,
            notes=notes,
            time=time,
            user_id=user_id,
            school_id=school_id,
            lesson_id=lesson_id)
    db.session.add(req)
    db.session.commit()
    return req
