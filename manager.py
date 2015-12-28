#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell
from myapp import app, db
from models import Student, Teacher, Course, Grade
from views import *


def make_shell_context():
    return dict(app=app, db=db, Student=Student, Teacher=Teacher,
                Course=Course, Grade=Grade)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
