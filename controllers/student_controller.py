from flask import Blueprint, render_template, session, redirect, url_for, request
from models import db, Student, Subject, RegisteredSubject, SubjectStructure

student_bp = Blueprint("student", __name__, template_folder="../templates/student")

# โปรไฟล์นักเรียน
@student_bp.route("/profile")
def profile():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    student_pk = session.get("student_id")
    if not student_pk:
        return redirect(url_for("login"))

    student = Student.query.get(student_pk)
    if not student:
        return redirect(url_for("login"))

    registered = RegisteredSubject.query.filter_by(student_id=student.id).all()
    return render_template("student/profile.html", student=student, registered=registered)

# หน้าลงทะเบียนเรียน
@student_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("role") != "student":
        return redirect(url_for("login"))
    student = Student.query.get(session["student_id"])
    registered_ids = [r.subject_id for r in student.registered_subjects]

    available = Subject.query.filter(~Subject.id.in_(registered_ids)).all()

    if request.method == "POST":
        subject_id = request.form.get("subject_id")
        reg = RegisteredSubject(student_id=student.id, subject_id=subject_id)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for("student.profile"))

    return render_template("student/register.html", student=student, available=available)
