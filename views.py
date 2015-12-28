# coding=utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user
from flask.ext.login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from models import Student, Teacher, Grade
from forms import *
from myapp import app, db


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if int(form.role.data) == 1:
            user = Student.query.get(form.id.data)
        else:
            user = Teacher.query.get(form.id.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(request.args.get('next') or url_for('home'))
        flash(u'账号或密码错误')
    # if user is already logined in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html', form=form)


@app.route('/home')
@login_required
def home():
    if current_user.__tablename__ == 'students':
        return render_template('stu_home.html')
    else:
        return render_template('teacher_home.html')


@app.route('/profile')
@login_required
def profile():
    if current_user.__tablename__ == 'students':
        user = Student.query.get(current_user.id)
        return render_template('stu_profile.html', user=user)
    else:
        user = Teacher.query.get(current_user.id)
        return render_template('teacher_profile.html', user=user)


@app.route('/grades')
@login_required
def grades():
    if current_user.__tablename__ == 'students':
        student = Student.query.get(current_user.id)
        grades = student.grades
        return render_template('own_grades.html', grades=grades)
    else:
        return render_template('404.html'), 404


@app.route('/all_stus')
@login_required
def all_stus():
    if current_user.__tablename__ == 'teachers':
        page = request.args.get('page', 1, type=int)
        pagination = Student.query.order_by(Student.id).paginate(
            page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
        stus = pagination.items
        return render_template('all_stus.html', stus=stus,
                               pagination=pagination)
    else:
        return render_template('404.html'), 404


@app.route('/all_grades')
@login_required
def all_grades():
    if current_user.__tablename__ == 'teachers':
        page = request.args.get('page', 1, type=int)
        pagination = Grade.query.order_by(Grade.stu_id).paginate(
            page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
        grades = pagination.items
        return render_template('all_grades.html', grades=grades,
                               pagination=pagination)
    else:
        return render_template('404.html'), 404


@app.route('/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade():
    if current_user.__tablename__ == 'teachers':
        form = GradeForm()
        if form.validate_on_submit():
            stu = Student.query.get(form.stu_id.data)
            if stu is None:
                flash(u'没有学号为 %s 的学生,请先创建该学生的信息'
                      % form.stu_id.data)
            else:
                stu_id = int(form.stu_id.data)
                course_id = form.course_id.data
                grade = form.grade.data
                new_grade = db.session.query(Grade).filter_by(
                    course_id=course_id, stu_id=stu_id).first()
                if new_grade is None:
                    new_grade = Grade(stu_id, course_id, grade)
                else:
                    new_grade.grade = grade
                try:
                    db.session.add(new_grade)
                    db.session.commit()
                except SQLAlchemyError:
                    flash(u'成绩添加失败，请确认输入是否正确')
                    db.session.rollback()
                else:
                    flash(u'成绩添加成功', 'success')
            return redirect(url_for('add_grade'))  # to clear form fields
        return render_template('add_grade.html', form=form)
    else:
        return render_template('404.html'), 404


@app.route('/update_grade', methods=['POST'])
@login_required
def update_grade():
    if current_user.__tablename__ == 'teachers':
        grade_id = int(request.form['grade_id'])
        new_grade = int(request.form['grade'])
        db.session.query(Grade).filter_by(id=grade_id).\
            update({"grade": new_grade})
        try:
            db.session.commit()
        except SQLAlchemyError:
            flash(u'成绩更新失败，请确认输入是否正确')
            db.session.rollback()
        return 'OK'  # view function must return a response, make it happy
    else:
        return render_template('404.html'), 404


@app.route('/delete_grade', methods=['POST'])
@login_required
def delete_grade():
    if current_user.__tablename__ == 'teachers':
        grade_id = request.form['id']
        grade = Grade.query.filter_by(id=grade_id).first()
        db.session.delete(grade)
        try:
            db.session.commit()
        except SQLAlchemyError:
            flash(u'成绩删除失败,请重试')
            db.session.rollback()
        return 'OK'
    else:
        return render_template('404.html'), 404


@app.route('/add_stu', methods=['GET', 'POST'])
@login_required
def add_stu():
    if current_user.__tablename__ == 'teachers':
        form = StudentForm()
        if form.validate_on_submit():
            new_stu = Student(form.stu_id.data,
                              form.name.data,
                              form.Class.data)
            try:
                db.session.add(new_stu)
                db.session.commit()
            except SQLAlchemyError:
                flash(u'已存在该学生的信息, 无法再进行新增')
                db.session.rollback()
            else:
                flash(u'新增成功', 'success')
            return redirect(url_for('add_stu'))  # to clear form fields
        return render_template('add_stu.html', form=form)
    else:
        return render_template('404.html'), 404


@app.route('/del_stu', methods=['GET', 'POST'])
@login_required
def del_stu():
    if current_user.__tablename__ == 'teachers':
        form = DelStudentForm()
        if form.validate_on_submit():
            stu = Student.query.get(form.stu_id.data)
            if stu is None:
                flash(u'没有学号为%s的学生' % form.stu_id.data)
            else:
                try:
                    db.session.delete(stu)
                    db.session.commit()
                except SQLAlchemyError:
                    flash(u'该学生还有成绩记录,请先删除成绩记录')
                    db.session.rollback()
                else:
                    flash(u'删除成功', 'success')
            return redirect(url_for('del_stu'))  # to clear form fields
        return render_template('del_stu.html', form=form)
    else:
        return render_template('404.html'), 404


@app.route('/change_passwd', methods=['GET', 'POST'])
@login_required
def change_passwd():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'密码修改成功', 'success')
        else:
            flash(u'旧密码错误,请重试')
    return render_template('change_passwd.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
