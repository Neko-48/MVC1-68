from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Student, Subject, RegisteredSubject

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

# --- Middleware ---
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Only admin can access this page")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

# --- หน้ารวมนักเรียน (default) ---
@admin_bp.route("/")
@admin_required
def students_list():
    q = request.args.get("q", "")
    sort = request.args.get("sort", "name")

    query = Student.query
    if q:
        query = query.filter(
            (Student.first_name.ilike(f"%{q}%")) |
            (Student.last_name.ilike(f"%{q}%")) |
            (Student.student_id.ilike(f"%{q}%"))
        )

    students = query.all()

    if sort == "name":
        students.sort(key=lambda s: (s.first_name, s.last_name))
    elif sort == "age":
        students.sort(key=lambda s: s.birthdate)

    return render_template("admin/students.html", students=students, q=q, sort=sort)

# --- ดูประวัตินักเรียน ---
@admin_bp.route("/student/<int:student_id>")
@admin_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("admin/student_detail.html", student=student)

# --- เลือกรายวิชาเพื่อกรอกเกรด ---
@admin_bp.route("/subjects")
@admin_required
def subjects_list():
    subjects = Subject.query.all()
    return render_template("admin/subjects.html", subjects=subjects)

# --- กรอกเกรดรายวิชา ---
@admin_bp.route("/grading/<int:subject_id>", methods=["GET", "POST"])
@admin_required
def grading(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    regs = RegisteredSubject.query.filter_by(subject_id=subject_id).all()

    if request.method == "POST":
        for reg in regs:
            grade_val = request.form.get(f"grade_{reg.id}")
            if grade_val:
                reg.grade = grade_val
        db.session.commit()
        flash("Grades updated successfully")
        return redirect(url_for("admin.grading", subject_id=subject_id))

    return render_template("admin/grading.html", subject=subject, regs=regs, count=len(regs))
