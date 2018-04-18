# services/users/manage.py


import unittest
import coverage


from flask_script import Manager
from flask_migrate import MigrateCommand
from project.api.models import School, Req, User
# from flask_graphql import GraphQLView


from project import create_app, db
from project.tests.utils import populate_school_db, populate_school_with_reqs
# from project.api.schema import schema

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()


app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=schema,
#         graphiql=True
#     )
# )


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def remove_reqs_MAO():
    """Deletes extant reqs"""
    user = User.query.filter_by(name='Oliver Mansell').first()
    reqs = Req.query.filter_by(user_id=user.id).all()
    for req in reqs:
        db.session.delete(req)
    db.session.commit()

@manager.command
def seed_db():

    school = School(name='Holy Family Catholic School')
    db.session.add(school)
    db.session.commit()

    populate_school_db(school.id)

    populate_school_with_reqs(school.id)

    db.session.add(School(name='testSchool'))

    db.session.commit()


if __name__ == '__main__':
    manager.run()
