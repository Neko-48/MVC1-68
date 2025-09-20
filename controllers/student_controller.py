from flask import Blueprint, render_template, session, redirect, url_for, request, flash
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
@student_bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register_subjects():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    # รายวิชาที่ยังไม่ได้ลง
    all_subjects = Subject.query.all()
    already_registered = [reg.subject_id for reg in student.registered_subjects]

    available_subjects = []
    for subj in all_subjects:
        if subj.id in already_registered:
            continue

        # ตรวจ prerequisite
        if subj.prerequisite_code:
            prereq = Subject.query.filter_by(subject_code=subj.prerequisite_code).first()
            if prereq:
                passed = RegisteredSubject.query.filter_by(
                    student_id=student.id, subject_id=prereq.id
                ).filter(RegisteredSubject.grade != "F").first()
                if not passed:
                    continue  # ยังไม่ผ่าน prerequisite → ห้ามลง

        available_subjects.append(subj)

    if request.method == "POST":
        subj_id = request.form.get("subject_id")
        subj = Subject.query.get(int(subj_id)) if subj_id else None
        if subj and subj in available_subjects:
            reg = RegisteredSubject(student_id=student.id, subject_id=subj.id, grade=None)
            db.session.add(reg)
            db.session.commit()
            flash("Subject registered successfully")
            return redirect(url_for("student.profile"))

    return render_template("student/register.html", student=student, subjects=available_subjects)