from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Student, Subject, RegisteredSubject, AdminUser

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
student_bp = Blueprint('student', __name__, url_prefix='/student')

# Simple auth decorator
from functools import wraps

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return "Forbidden", 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Admin Views
@admin_bp.route('/students')
@login_required(role='admin')
def admin_students():
    q = request.args.get('q')
    school = request.args.get('school')
    sort = request.args.get('sort') # 'name' or 'age'

    query = Student.query
    if q:
        query = query.filter((Student.first_name.ilike(f"%{q}%")) | (Student.last_name.ilike(f"%{q}%")))
    if school:
        query = query.filter_by(school=school)
    students = query.all()
    # simple sorting
    if sort == 'name':
        students.sort(key=lambda s: (s.first_name, s.last_name))
    elif sort == 'age':
        students.sort(key=lambda s: s.birth_date or '9999-99-99')

    return render_template('admin_students.html', students=students)

@admin_bp.route('/grading/<int:subject_id>', methods=['GET','POST'])
@login_required(role='admin')
def admin_grading(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    regs = RegisteredSubject.query.filter_by(subject_id=subject_id).all()
    if request.method == 'POST':
    # process grades
        for reg in regs:
            grade = request.form.get(f'grade_{reg.id}')
            reg.grade = grade if grade else reg.grade
        db.session.commit()
        flash('Grades saved')
        return redirect(url_for('admin.admin_grading', subject_id=subject_id))

    return render_template('admin_grading.html', subject=subject, regs=regs)

# Student Views
@student_bp.route('/profile')
@login_required(role='student')
def student_profile():
    student_id = session.get('student_id')
    student = Student.query.get_or_404(student_id)
    return render_template('student_profile.html', student=student)


@student_bp.route('/register', methods=['GET','POST'])
@login_required(role='student')
def student_register():
    student_id = session.get('student_id')
    student = Student.query.get_or_404(student_id)

    # show subjects in student's curriculum that are not yet registered
    registered_subject_ids = [r.subject_id for r in student.registered_subjects]
    available = Subject.query.filter_by(curriculum=student.curriculum).filter(~Subject.id.in_(registered_subject_ids)).all()

    if request.method == 'POST':
        subj_id = int(request.form.get('subject_id'))
        # basic business rules: must not register if prereq not satisfied
        subj = Subject.query.get_or_404(subj_id)
        if subj.prerequisite_subject_id:
            # check if student has passed prerequisite
            passed = any((r.subject_id == subj.prerequisite_subject_id and r.grade and r.grade != 'F') for r in student.registered_subjects)
            if not passed:
                flash('Prerequisite not satisfied')
                return redirect(url_for('student.student_register'))

        reg = RegisteredSubject(student_id=student.id, subject_id=subj.id)
        db.session.add(reg)
        db.session.commit()
        flash('Registered')
        return redirect(url_for('student.student_register'))

    return render_template('student_register.html', student=student, available=available)