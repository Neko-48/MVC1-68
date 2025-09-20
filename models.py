from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RegisteredSubject(db.Model):
    __tablename__ = "registered_subjects"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    grade = db.Column(db.String(2))

    # ความสัมพันธ์กลับไปหา Student และ Subject
    student = db.relationship("Student", back_populates="registered_subjects")
    subject = db.relationship("Subject", back_populates="registered_subjects")


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(8), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    school = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    curriculum_code = db.Column(db.String(20), nullable=False)

    # back_populates ต้องตรงกับ RegisteredSubject
    registered_subjects = db.relationship("RegisteredSubject", back_populates="student", cascade="all, delete-orphan")
    # property รวมชื่อ
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    # property คำนวณอายุ
    @property
    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )

class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(8), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    prerequisite_code = db.Column(db.String(8), nullable=True)

    # back_populates ต้องตรงกับ RegisteredSubject
    registered_subjects = db.relationship("RegisteredSubject", back_populates="subject")


class SubjectStructure(db.Model):
    __tablename__ = "subject_structures"
    id = db.Column(db.Integer, primary_key=True)
    curriculum_code = db.Column(db.String(8), nullable=False)
    curriculum_name = db.Column(db.String(120), nullable=False)
    department_name = db.Column(db.String(120), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, default=1)

    subject = db.relationship("Subject", backref="structures")


class AdminUser(db.Model):
    __tablename__ = "admin_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
