# encoding=utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from myapp import app, login_manager, db


class Student(UserMixin, db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    Class = db.Column(db.Unicode)
    password_hash = db.Column(db.String(128))
    grades = db.relationship('Grade', backref='student', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, id, name, Class, password=app.config['DEFAULT_PASSWD']):
        self.id = id
        self.name = name
        self.Class = Class
        self.password_hash = password

    def __repr__(self):
        return '<Student %r>' % self.id


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password_hash = password

    def __repr__(self):
        return '<Teacher %r>' % self.id


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    grades = db.relationship('Grade', backref='course', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Course %r>' % self.id


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, unique=True)
    stu_id = db.Column(db.Integer, db.ForeignKey('students.id'),
                       primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
                          primary_key=True)
    grade = db.Column(db.Integer)

    def __init__(self, stu_id, course_id, grade):
        self.stu_id = stu_id
        self.course_id = course_id
        self.grade = grade

    def __repr__(self):
        return '<Grade %r, %r, %r>' % \
            (self.stu_id, self.course_id, self.grade)


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id)) or Teacher.query.get(int(user_id))
