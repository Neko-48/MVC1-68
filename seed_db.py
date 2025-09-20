from app import app, db
from models import Student, Subject, SubjectStructure, RegisteredSubject, AdminUser
from datetime import date

def get_subject(subject_code):
    return Subject.query.filter_by(subject_code=subject_code).first()

def get_student(student_id):
    return Student.query.filter_by(student_id=student_id).first()

def seed():
     with app.app_context(): 
        db.drop_all()
        db.create_all()

        # ---------- Admin ----------
        admin = AdminUser(username="admin", password="admin123")
        db.session.add(admin)

        # ---------- Students ----------
        students = [
            Student(student_id="69000001", first_name="Anan", last_name="Wongchai",
                    birthdate=date(2006, 5, 12), school="Satriwitthaya",
                    email="anan@example.com", curriculum_code="CURR001"),
            Student(student_id="69000002", first_name="Somchai", last_name="Jaidee",
                    birthdate=date(2007, 8, 20), school="Triamudom",
                    email="somchai@example.com", curriculum_code="CURR001"),
            Student(student_id="69000003", first_name="Suda", last_name="Meechai",
                    birthdate=date(2006, 1, 15), school="Yothinburana",
                    email="suda@example.com", curriculum_code="CURR002"),
            Student(student_id="69000004", first_name="Kamol", last_name="Thongdee",
                    birthdate=date(2006, 9, 18), school="Suankularb",
                    email="kamol@example.com", curriculum_code="CURR001"),
            Student(student_id="69000005", first_name="Nicha", last_name="Srichai",
                    birthdate=date(2007, 2, 1), school="Debsirin",
                    email="nicha@example.com", curriculum_code="CURR002"),
            Student(student_id="69000006", first_name="Chanin", last_name="Yimyai",
                    birthdate=date(2006, 4, 7), school="Bodindecha",
                    email="chanin@example.com", curriculum_code="CURR001"),
            Student(student_id="69000007", first_name="Ploy", last_name="Siriwat",
                    birthdate=date(2007, 11, 25), school="Assumption",
                    email="ploy@example.com", curriculum_code="CURR002"),
            Student(student_id="69000008", first_name="Kittipong", last_name="Saelee",
                    birthdate=date(2006, 3, 2), school="Vajiravudh",
                    email="kitti@example.com", curriculum_code="CURR001"),
            Student(student_id="69000009", first_name="Supansa", last_name="Rattanak",
                    birthdate=date(2006, 6, 11), school="St. Joseph",
                    email="supansa@example.com", curriculum_code="CURR002"),
            Student(student_id="69000010", first_name="Arthit", last_name="Meechai",
                    birthdate=date(2007, 7, 30), school="Suankularb",
                    email="arthit@example.com", curriculum_code="CURR001"),
        ]
        db.session.add_all(students)

        # ---------- Subjects ----------
        subjects = [
            Subject(subject_code="05500001", name="Calculus I", credit=3, instructor="Dr. Anucha",
                    prerequisite_code=None),
            Subject(subject_code="05500002", name="Physics I", credit=3, instructor="Dr. Somchai",
                    prerequisite_code=None),
            Subject(subject_code="05500003", name="Chemistry I", credit=3, instructor="Dr. Suda",
                    prerequisite_code=None),
            Subject(subject_code="90690001", name="English I", credit=3, instructor="Dr. Kamol",
                    prerequisite_code=None),
            Subject(subject_code="90690002", name="Thai Civilization", credit=2, instructor="Dr. Nicha",
                    prerequisite_code=None),
            Subject(subject_code="90690005", name="History of Asia", credit=2, instructor="Dr. Chanin",
                    prerequisite_code=None),
            Subject(subject_code="05500004", name="Computer Programming", credit=3, instructor="Dr. Ploy",
                    prerequisite_code="05500001"),
            Subject(subject_code="05500005", name="Linear Algebra", credit=3, instructor="Dr. Kittipong",
                    prerequisite_code="05500001"),
            Subject(subject_code="90690003", name="English II", credit=3, instructor="Dr. Supansa",
                    prerequisite_code="90690001"),
            Subject(subject_code="90690004", name="Psychology", credit=2, instructor="Dr. Arthit",
                    prerequisite_code=None),
            Subject(subject_code="05500006", name="Biology I", credit=3, instructor="Dr. Arisa",
                    prerequisite_code=None),
        ]
        db.session.add_all(subjects)
        db.session.commit()

        # ---------- SubjectStructure ----------
        structures = [
            SubjectStructure(curriculum_code="10000001", curriculum_name="Science Program",
                            department_name="Mathematics", subject_id=get_subject("05500001").id, semester=1),
            SubjectStructure(curriculum_code="10000001", curriculum_name="Science Program",
                            department_name="Physics", subject_id=get_subject("05500002").id, semester=1),
            SubjectStructure(curriculum_code="10000001", curriculum_name="Science Program",
                            department_name="Chemistry", subject_id=get_subject("05500003").id, semester=1),
            SubjectStructure(curriculum_code="20000001", curriculum_name="General Education",
                            department_name="Languages", subject_id=get_subject("90690001").id, semester=1),
            SubjectStructure(curriculum_code="20000001", curriculum_name="General Education",
                            department_name="Humanities", subject_id=get_subject("90690002").id, semester=1),
            SubjectStructure(curriculum_code="20000001", curriculum_name="General Education",
                            department_name="History", subject_id=get_subject("90690005").id, semester=1),
            SubjectStructure(curriculum_code="10000001", curriculum_name="Science Program",
                            department_name="Computer Science", subject_id=get_subject("05500004").id, semester=2),
            SubjectStructure(curriculum_code="10000001", curriculum_name="Science Program",
                            department_name="Mathematics", subject_id=get_subject("05500005").id, semester=2),
            SubjectStructure(curriculum_code="10000001", curriculum_name="Science Program",
                            department_name="Biology", subject_id=get_subject("05500006").id, semester=2),
            SubjectStructure(curriculum_code="20000001", curriculum_name="General Education",
                            department_name="Languages", subject_id=get_subject("90690003").id, semester=2),
            SubjectStructure(curriculum_code="20000001", curriculum_name="General Education",
                            department_name="Psychology", subject_id=get_subject("90690004").id, semester=2),
        ]
        db.session.add_all(structures)
        db.session.commit()
        # ---------- RegisteredSubject ----------
        registered = [
            RegisteredSubject(student_id=get_student("69000001").id, subject_id=get_subject("05500001").id, grade="A"),
            RegisteredSubject(student_id=get_student("69000001").id, subject_id=get_subject("05500002").id, grade="B+"),
            RegisteredSubject(student_id=get_student("69000002").id, subject_id=get_subject("05500001").id, grade="C"),
            RegisteredSubject(student_id=get_student("69000002").id, subject_id=get_subject("90690001").id, grade="A"),
            RegisteredSubject(student_id=get_student("69000003").id, subject_id=get_subject("90690002").id, grade="B"),
            RegisteredSubject(student_id=get_student("69000004").id, subject_id=get_subject("05500003").id, grade="D+"),
            RegisteredSubject(student_id=get_student("69000005").id, subject_id=get_subject("05500002").id, grade="F"),
            RegisteredSubject(student_id=get_student("69000006").id, subject_id=get_subject("05500004").id, grade="A"),
            RegisteredSubject(student_id=get_student("69000007").id, subject_id=get_subject("05500005").id, grade="B+"),
            RegisteredSubject(student_id=get_student("69000008").id, subject_id=get_subject("90690003").id, grade="C+"),
        ]
        db.session.add_all(registered)

        db.session.commit()
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed()
