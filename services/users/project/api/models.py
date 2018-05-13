# services/users/project/api/models.py

import datetime
import jwt
from flask import current_app
from project import db, bcrypt
from sqlalchemy.orm import relationship
from project.api.constants import PREFERENCES_TEMPLATE, TEACHER
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    staff_code = db.Column(db.String(5), nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role_code = db.Column(db.Integer, default=TEACHER, nullable=False)

    admin = db.Column(db.Boolean, default=False, nullable=False)

    active = db.Column(db.Boolean, default=False)

    school_id = db.Column(
        db.Integer,
        db.ForeignKey('schools.id')
    )
    school = relationship("School", foreign_keys=[school_id])

    lessons = db.relationship(
        "Lesson",
        primaryjoin="User.id==Lesson.teacher_id",
        backref='teacher_of',
        lazy='dynamic'
    )
    # done_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # done_by = relationship("User", foreign_keys=[done_by_id])

    reqs = db.relationship(
        'Req',
        primaryjoin='User.id==Req.user_id',
        backref='teacher',
        lazy='dynamic'
    )

    # TECHNICIAN BACKREF TO COMPLETED REQS
    reqs_completed = db.relationship(
        'Req',
        primaryjoin='User.id==Req.done_by_id',
        backref='technician_done',
        lazy='dynamic'
    )

    req_issues = db.relationship(
        'Req',
        primaryjoin='User.id==Req.issue_technician_id',
        backref='technician_issue',
        lazy='dynamic')

    def __init__(
        self, user_info
    ):
        self.name = user_info['name']
        self.email = user_info['email']
        self.password = bcrypt.generate_password_hash(
            user_info['password'], current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.role_code = user_info['role_code']
        try:
            self.staff_code = user_info['staff_code']
        except KeyError:
            pass
        try:
            self.school_id = user_info['school_id']
        except KeyError:
            pass
        try:
            self.admin = user_info['admin']
        except KeyError:
            self.admin = False


    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token - :param auth_token: - :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class School(db.Model):

    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    reqs = db.relationship(
        'Req',
        primaryjoin='School.id==Req.school_id',
        backref='school_from_req',
        lazy='dynamic')

    rooms = db.relationship(
        'Room',
        primaryjoin='School.id==Room.school_id',
        lazy='dynamic'
    )
    classgroups = db.relationship(
        'Classgroup',
        primaryjoin='School.id==Classgroup.school_id',
        lazy='dynamic'
    )
    sites = db.relationship(
        'Site',
        primaryjoin='School.id==Site.school_id',
        lazy='dynamic'
    )
    lessons = db.relationship(
        'Lesson',
        primaryjoin='School.id==Lesson.school_id',
        lazy='dynamic'
    )

    preferences = db.Column(JSON)

    def __init__(self, name):
        self.name = name
        self.preferences = PREFERENCES_TEMPLATE


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = relationship("Room", foreign_keys=[room_id])

    school_id = db.Column(
        db.Integer, db.ForeignKey('schools.id'), nullable=False
    )
    school = relationship("School", foreign_keys=[school_id])

    classgroup_id = db.Column(
        db.Integer, db.ForeignKey('classgroups.id'), nullable=False
    )
    classgroup = relationship("Classgroup", foreign_keys=[classgroup_id])

    teacher_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    teacher = relationship("User", foreign_keys=[teacher_id])

    period = db.Column(db.Integer)

    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    day_code = db.Column(db.Integer, nullable=False)  # ISODAY FORMAT: MON 1
    week_number = db.Column(db.Integer, default=1)


class Classgroup(db.Model):
    __tablename__ = 'classgroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    school_id = db.Column(
        db.Integer,
        db.ForeignKey('schools.id')
    )
    school = relationship("School", foreign_keys=[school_id])

    lessons = db.relationship(
        'Lesson',
        primaryjoin='Classgroup.id==Lesson.classgroup_id',
        lazy='dynamic'
        )


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    school_id = db.Column(
        db.Integer,
        db.ForeignKey('schools.id'),
        nullable=False
    )
    school = relationship("School", foreign_keys=[school_id])

    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True)
    site = relationship("Site", foreign_keys=[site_id])

    lessons = db.relationship(
        "Lesson",
        primaryjoin='Room.id==Lesson.room_id',
        lazy='dynamic'
    )


class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    school_id = db.Column(
        db.Integer,
        db.ForeignKey('schools.id'),
        nullable=False
    )
    school = relationship("School", foreign_keys=[school_id])


class Req(db.Model):

    __tablename__ = 'reqs'

    id = db.Column(db.Integer, primary_key=True)
    submitted_at = db.Column(db.DateTime,  default=datetime.datetime.utcnow)

    # details of requisition
    title = db.Column(db.String(1000), nullable=False)
    equipment = db.Column(db.String(1000), nullable=True)
    notes = db.Column(db.String(1000), nullable=True)

    time = db.Column(db.DateTime, nullable=False)

    hasIssue = db.Column(db.Boolean, default=False)
    issue_text = db.Column(db.String(1000))
    issue_technician_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    issue_technician = relationship("User", foreign_keys=[issue_technician_id])

    isDone = db.Column(db.Boolean, default=False)
    done_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    done_by = relationship("User", foreign_keys=[done_by_id])
    done_at = db.Column(db.DateTime)

    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    lesson = relationship("Lesson", foreign_keys=[lesson_id])
    # links
    # ttlesson_id = db.Column(db.Integer, db.ForeignKey('timetabledlesson.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[user_id])

    school_id = db.Column(
        db.Integer,
        db.ForeignKey('schools.id'),
        nullable=False)
    school = relationship("School", foreign_keys=[school_id])

    def __init__(
        self, title, equipment, notes, time, user_id, school_id,
            lesson_id=None):
        self.title = title,
        self.equipment = equipment,
        self.notes = notes,
        self.time = time,
        self.user_id = user_id,
        self.school_id = school_id,
        self.lesson_id = lesson_id
