# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Regexp, NumberRange
from models import Course


class LoginForm(Form):
    id = StringField(u'账号', validators=[DataRequired(),
                     Regexp(r'\d{10}',
                     message=u'请输入10位的账号')])
    password = PasswordField(u'密码', validators=[DataRequired()])
    role = RadioField('role', validators=[DataRequired()],
                      choices=[('1', u'学生'), ('2', u'教师')],
                      default='1')
    remeber_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class StudentForm(Form):
    stu_id = StringField(u'学号', validators=[DataRequired(),
                         Regexp(r'\d{10}',
                         message=u'请输入10位的学号')])
    name = StringField(u'姓名', validators=[DataRequired(u'请输入姓名')])
    Class = StringField(u'班级', validators=[DataRequired(u'请输入班级')])
    submit = SubmitField(u'确认')


class DelStudentForm(Form):
    stu_id = StringField(u'学号', validators=[DataRequired(),
                         Regexp(r'\d{10}',
                         message=u'请输入10位的学号')])
    submit = SubmitField(u'删除')


class GradeForm(Form):
    stu_id = StringField(u'学号', validators=[DataRequired(),
                         Regexp(r'\d{10}',
                         message=u'请输入10位的学号')])
    course_id = SelectField(u'课程', coerce=int, validators=[DataRequired()],
            choices=[(c.id, c.name) for c in Course.query.order_by('id')])
    grade = IntegerField(u'分数', validators=[DataRequired(),
                         NumberRange(0, 100, u'分数只能在0-100之间')])
    submit = SubmitField(u'确认')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[DataRequired()])
    submit = SubmitField(u'确认')
