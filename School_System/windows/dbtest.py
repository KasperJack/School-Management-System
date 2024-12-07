import sqlite3

import os


def connect():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'school.db')

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")

    return db_path


import sqlite3


def get_class_info(class_name):
    db_path = connect()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    student_query = """
    SELECT s.full_name
    FROM students s
    JOIN class c ON s.class_name = c.class_name
    WHERE c.class_name = ?;
    """

    cursor.execute(student_query, (class_name,))
    students = cursor.fetchall()
    student_names = [full_name for full_name, in students]

    subject_teacher_query = """
    SELECT t.full_name AS teacher, sub.subject_name AS subject
    FROM teachers_subjects ts
    JOIN teachers t ON ts.teacher_id = t.teacher_id
    JOIN subjects sub ON ts.subject_id = sub.subject_id
    JOIN course crs ON crs.id = ts.subject_id
    WHERE crs.class_name = ?;
    """

    cursor.execute(subject_teacher_query, (class_name,))
    subject_teacher_pairs = cursor.fetchall()

    subject_teacher_list = [(teacher, subject) for teacher, subject in subject_teacher_pairs]

    subject_teacher_dict = {}
    for teacher, subject in subject_teacher_pairs:
        if teacher not in subject_teacher_dict:
            subject_teacher_dict[teacher] = []
        subject_teacher_dict[teacher].append(subject)

    conn.close()

    #  result
    return student_names, subject_teacher_dict  # You can also return subject_teacher_list if preferred




cclass_name =  "class 05"

students, subject_teachers = get_class_info(cclass_name)

print("Students:", students)
print("Teacher-Subject Pairings:", subject_teachers)
