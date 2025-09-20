from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Student, AdminUser
from controllers.admin_controller import admin_bp
from controllers.student_controller import student_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# --- Register Blueprints ---
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(student_bp, url_prefix="/student")

# --- Home Redirect ---
@app.route("/")
def index():
    if "role" in session:
        if session["role"] == "admin":
            return redirect(url_for("admin.students_list"))  # หน้าแรกของแอดมิน
        elif session["role"] == "student":
            return redirect(url_for("student.profile"))      # หน้าแรกของนักเรียน
    return redirect(url_for("login"))

# --- Login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        if role == "admin":
            admin = AdminUser.query.filter_by(username=username, password=password).first()
            if admin:
                session["role"] = "admin"
                session["admin_id"] = admin.id
                flash("Welcome Admin!")
                return redirect(url_for("admin.students_list"))

        elif role == "student":
        # ใช้ student_id แทน student_code ให้ตรงกับ seed_db.py
            student = Student.query.filter_by(student_id=username).first()
            if student and password == "studentpass":  # mock password ทุกคนใช้ studentpass
                session["role"] = "student"
                session["student_id"] = student.id
                flash(f"Welcome {student.first_name}!")
                return redirect(url_for("student.profile"))

        flash("Invalid credentials")
    return render_template("login.html")

# --- Logout ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
