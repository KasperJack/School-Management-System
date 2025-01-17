
import sqlite3
from School_System.db import DB_PATH
from datetime import datetime
from collections import defaultdict


LOGGED_IN_USER_NAME = None
LOGGED_IN_USER_ID = None
PROFILE_PIC = None



# constants for return values
SUPERADMIN = "superadmin"
ADMIN = "admin"
USER_INACTIVE = "inactive"
INVALID_CREDENTIALS = "invalid"


def login_user(email, password):
    ######## connect to the database ########
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query the database for the user
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:
            status = result[5]  # Status column
            user_type = result[4] # User type column
            id = result[0]
            name = result[1]
            if status == 'inactive':  # explicit check for inactive users
                return USER_INACTIVE
            if status == 'active':
                if user_type == 'superadmin':
                    log_user_in(id)
                    return SUPERADMIN
                elif user_type == 'admin':
                    log_user_in(id)
                    return ADMIN


        return INVALID_CREDENTIALS  # gitaddno match is found




#adds a user to the db (admin)
def add_account_user(full_name, email, password):

    try:
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()
            
            # Insert user into the database
            query = """
                INSERT INTO users (full_name, email, password) 
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (full_name, email, password))
            db_connection.commit()
            return "User added successfully"
    except sqlite3.IntegrityError:
        return "This email already exists"
    except Exception as e:
        return f"{e}"
    

#retunrs a list of inactive users (admins)
def get_inactive_admins():
    # Connect to the database
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch inactive users
        query = """
            SELECT full_name, email, registration_date 
            FROM users 
            WHERE status = 'inactive'
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results


def delete_admin(full_name,email):
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE full_name = ? AND email = ?", (full_name, email))
        db_connection.commit()






def activate_admin(full_name,email):
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("UPDATE users SET status = 'active' WHERE full_name = ? AND email = ?", (full_name, email))
        db_connection.commit()




#adds admin the entry log
def log_user_in(user_id):
    # Connect to the database
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        #cursor.execute("DELETE FROM logged_in_user")
        query = """
            SELECT user_id, full_name, email, type 
            FROM users 
            WHERE user_id = ?
        """
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            insert_query = """
                INSERT OR REPLACE INTO logged_in_user (id, full_name, email, type)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_query, user_data)
            db_connection.commit()
            global LOGGED_IN_USER_ID , LOGGED_IN_USER_NAME
            LOGGED_IN_USER_ID = user_data[0]
            LOGGED_IN_USER_NAME = user_data[1]
            #print(LOGGED_IN_USER_NAME)
            #print(LOGGED_IN_USER_ID)
        else:
            raise ValueError(f"User with ID {user_id} not found.")





#### not in use ??
def clear_entry_log():
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query to find the most recent entry by timestamp
        query_get_last = "SELECT MAX(time) FROM logged_in_user"
        cursor.execute(query_get_last)
        last_timestamp = cursor.fetchone()[0]

        if last_timestamp is not None:
            # Delete all other entries except the one with the most recent timestamp
            query_delete = "DELETE FROM logged_in_user WHERE time != ?"
            cursor.execute(query_delete, (last_timestamp,))
            db_connection.commit()


def add_subject(subject_name,description=None):
    # Connect to the database
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Insert query to add a new subject
        query = """
            INSERT INTO subjects (subject_name, description) 
            VALUES (?, ?)
        """
        try:
            cursor.execute(query, (subject_name, description))
            db_connection.commit()
            activity_type = "add"
            affected_entity = "subject"
            entity_name = subject_name
            entity_id = get_subjects_sequence()
            additional_info = "blablabla  N/A"
            log_activity(activity_type, affected_entity, entity_name, entity_id, additional_info,db_connection)
            return "Subject added successfully"
        except sqlite3.Error as e:
            return f"{e}"




def add_teacher(full_name, phone, email, gender, address=None):
    try:

        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()

            # SQL query to insert a teacher
            query = """
            INSERT INTO teachers (full_name, phone, email, gender, address)
            VALUES (?, ?, ?, ?, ?);
            """

            # Execute the query with the provided data
            cursor.execute(query, (full_name, phone, email, gender, address))

            # Commit the changes
            db_connection.commit()
            activity_type = "add"
            affected_entity = "teacher"
            entity_name = full_name
            entity_id = get_teachers_sequence()
            additional_info = "blablabla"
            log_activity(activity_type, affected_entity, entity_name, entity_id, additional_info,db_connection)

        return "Teacher added successfully"

    except sqlite3.IntegrityError as e:
        # Handle unique constraint violations (e.g., duplicate phone or email)
        return f"{e}"

    except sqlite3.Error as e:
        return f"{e}"



def get_subjects():
    """Fetch subjects from the database and populate the subjects_scrollArea with checkboxes."""
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT subject_id, subject_name FROM subjects")
        subjects = cursor.fetchall()
    return subjects






def update_teachers_count():
    pass



def add_teacher_subject(teacher_id, subject_id):
    """
    Insert a teacher's subject into the teachers_subjects table.
    """
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        try:
            # Insert the data into the teachers_subjects table
            cursor.execute(
                "INSERT INTO teachers_subjects (teacher_id, subject_id) VALUES (?, ?)",
                (teacher_id, subject_id)
            )
            db_connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            return False

#ts_id #class_id
def add_course(teacher_subject,class_name):
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        try:
            # Insert the data into the teachers_subjects table
            cursor.execute(
                "INSERT INTO course (ts_id, class_id) VALUES (?, ?)",
                (teacher_subject, class_name))
            db_connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            return False



def get_grades():
    """Fetch grade names from the grades table and return them as a list."""

    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT grade_name FROM grades")
        grades = cursor.fetchall()  # Fetch all grade names
        grades = [grade[0] for grade in grades]
    return  grades




def add_class(class_name, grade_name, session, max_students):
    """
    Insert a new class with the given class_name and grade_name into the class table.
    """


    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        try:
            # Insert the new class into the class table
            cursor.execute(
                "INSERT INTO class (class_name, grade_name, session, max_students) VALUES (?, ?, ?, ?)",
                (class_name, grade_name, session, max_students)
            )
            db_connection.commit()
            db_connection.commit()
            activity_type = "add"
            affected_entity = "class"
            entity_name = class_name
            entity_id = get_classes_sequence()
            additional_info = "blablabla"
            log_activity(activity_type, affected_entity, entity_name, entity_id, additional_info,db_connection)
            return "Class added successfully"
        except sqlite3.IntegrityError as e:
            return f"{e}"




def get_teachers_sequence():



    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch the sequence number for 'teachers'
        query = "SELECT seq FROM sqlite_sequence WHERE name = 'teachers';"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

    # Return the sequence number if found, else None
    return result[0] if result else None




def get_students_sequence():

    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch the sequence number for 'students'
        query = "SELECT seq FROM sqlite_sequence WHERE name = 'students';"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

    # Return the sequence number if found, else None
    return result[0] if result else None



def get_subjects_sequence():



    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch the sequence number for 'students'
        query = "SELECT seq FROM sqlite_sequence WHERE name = 'subjects';"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

    # Return the sequence number if found, else None
    return result[0] if result else None






def get_classes_sequence():



    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch the sequence number for 'students'
        query = "SELECT seq FROM sqlite_sequence WHERE name = 'class';"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

    # Return the sequence number if found, else None
    return result[0] if result else None
















def get_classes():
    """Fetch a list of class names from the database."""


    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        # Query to fetch all class names
        cursor.execute("SELECT class_name FROM class")
        classes = cursor.fetchall()
        classes = [class_name[0] for class_name in classes]

    return classes










def get_classes_ids():
    """Fetch a list of (class_id, class_name) from the database."""
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        # Query to fetch class IDs and names
        cursor.execute("SELECT class_id, class_name FROM class")
        classes = cursor.fetchall()  # List of tuples (class_id, class_name)

    return classes





def add_student(full_name, phone, email, gender, birth_date, address, class_id=None, photo =None):
    """
    Inserts a new student into the `students` table and handles integrity errors.
    """
    try:
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()


            cursor.execute(
                """
                INSERT INTO students (full_name, phone, email, gender, birth_date, address, class_id, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (full_name, phone, email, gender, birth_date, address, class_id, photo)
            )

            # commit
            db_connection.commit()
            activity_type = "add"
            affected_entity = "student"
            entity_name = full_name
            entity_id = get_students_sequence()
            additional_info = "blablabla"
            log_activity(activity_type, affected_entity, entity_name, entity_id, additional_info,db_connection)
            return "Student added successfully"

    except sqlite3.IntegrityError as e:
        #integrity errors ( foreign key violations, unique constraint failures)
        return f"{e}"
    except Exception as e:
        #handle other database errors
        return f"{e}"



def get_total_students():
    try:
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()

            #count the total number of students
            cursor.execute("SELECT COUNT(*) FROM students")
            total_students = cursor.fetchone()[0]

            return total_students

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None  # None if there is an error


def get_total_teachers():
    try:
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()

            #count the total number of teachers
            cursor.execute("SELECT COUNT(*) FROM teachers")
            total_teachers = cursor.fetchone()[0]  #

            return total_teachers

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None  #none if there is an error



def get_total_classes():
    try:
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()

            # Query to count the total number of classes
            cursor.execute("SELECT COUNT(*) FROM class")
            total_classes = cursor.fetchone()[0]  # Fetch the first result of the query

            return total_classes

    except sqlite3.Error as e:
        return None  # Return None if there is an error


def get_students_info():
    """Fetch student information and populate the students_table."""
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        # Corrected query to fetch student info with grade and class name
        query = """
        SELECT 
            students.student_id,
            students.full_name,
            grades.grade_name,
            class.class_name,
            students.birth_date,
            students.address,
            students.phone,
            students.email
        FROM 
            students
        LEFT JOIN 
            class ON students.class_id = class.class_id
        LEFT JOIN 
            grades ON class.grade_name = grades.grade_name
        """
        cursor.execute(query)
        students = cursor.fetchall()
        return students





def get_teachers_subjects():
    """Fetch teacher-subject pairs from the database and populate the teachers_subjects_scrollArea with checkboxes."""
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        # Query to fetch teacher-subject pairs
        cursor.execute("""
            SELECT ts.ts_id, sub.subject_name, t.full_name
            FROM teachers_subjects ts
            JOIN subjects sub ON ts.subject_id = sub.subject_id
            JOIN teachers t ON ts.teacher_id = t.teacher_id
        """)
        teachers_subjects = cursor.fetchall()
        return  teachers_subjects



def get_student_details(student_id):
    """
    Fetch detailed information about a specific student, including class name.

    Args:
        student_id (int): The ID of the student to fetch details for.

    Returns:
        dict: A dictionary containing student details if found.
        str: An error message if no student is found or a database error occurs.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Query to fetch student details, including the class name
        query = """
        SELECT 
            students.photo, 
            students.full_name, 
            students.phone, 
            students.email, 
            students.birth_date, 
            students.address, 
            class.class_name, 
            students.registration_date, 
            students.additional_info
        FROM 
            students
        LEFT JOIN 
            class ON students.class_id = class.class_id
        WHERE 
            students.student_id = ?;
        """
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()

        # If a student with the given ID exists, return the details
        if result:
            student_details = {
                "photo": result[0],
                "full_name": result[1],
                "phone": result[2],
                "email": result[3],
                "birth_date": result[4],
                "address": result[5],
                "class_name": result[6],  # Fetched from the class table
                "registration_date": result[7],
                "additional_info": result[8],
            }
            return student_details
        else:
            return f"No student found with ID {student_id}"

    except sqlite3.Error as e:
        return f"Database error: {e}"

    finally:
        conn.close()




def delete_student(student_id, student_name):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Delete student query
            delete_query = "DELETE FROM students WHERE student_id = ?"
            cursor.execute(delete_query, (student_id,))

            if cursor.rowcount > 0:
                # Log the activity using the same connection
                activity_type = "delete"
                affected_entity = "student"
                entity_name = student_name
                entity_id = student_id
                additional_info = "blablabla"
                log_activity(
                    activity_type,
                    affected_entity,
                    entity_name,
                    entity_id,
                    additional_info,
                    conn  # Pass the shared connection
                )

                return "Student has been deleted successfully."
            else:
                return "No student found."  # Could include more details if needed

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return "An error occurred while trying to delete the student."


def log_activity(activity_type, affected_entity, entity_name, entity_id, additional_info=None, conn=None):
    """
    Logs user activity into the activity_log table.

    Args:
        activity_type (str): Type of activity performed.
        affected_entity (str): Entity affected by the activity (e.g., 'student', 'class').
        entity_name (str): Name of the affected entity.
        entity_id (int): ID of the affected entity.
        additional_info (str, optional): Additional information about the activity.
        conn (sqlite3.Connection, optional): Database connection to use. If not provided, a new one will be created.
    """
    try:
        # Track whether the connection was created in this function
        created_connection = False

        # Use the existing connection if provided, otherwise create a new one
        if conn is None:
            conn = sqlite3.connect(DB_PATH)
            created_connection = True

        cursor = conn.cursor()

        # Insert activity log query
        insert_query = """
        INSERT INTO activity_log (
            timestamp, user_id, user_name, activity_type, 
            affected_entity, entity_name, entity_id, additional_info
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?
        )
        """
        # Get logged-in user details
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Execute the query
        cursor.execute(
            insert_query,
            (timestamp, LOGGED_IN_USER_ID, LOGGED_IN_USER_NAME, activity_type, affected_entity, entity_name, entity_id, additional_info)
        )

        # Commit changes only if using a new connection
        if created_connection:
            conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred in log_activity: {e}")

    finally:
        # Close the connection only if it was created in this function
        if created_connection:
            conn.close()




def get_activity_log():

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        #excluding the "additional_info"
        query = """
        SELECT log_id, timestamp, user_id, user_name, 
               activity_type, affected_entity, entity_name, entity_id 
        FROM activity_log_view
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        connection.close()
        return rows

    except sqlite3.Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"






def get_teachers_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT 
        t.teacher_id, 
        t.full_name AS teacher_name,
        s.subject_name,
        c.class_name
    FROM teachers t
    LEFT JOIN teachers_subjects ts ON t.teacher_id = ts.teacher_id
    LEFT JOIN subjects s ON ts.subject_id = s.subject_id
    LEFT JOIN course co ON ts.ts_id = co.ts_id
    LEFT JOIN class c ON co.class_id = c.class_id;
    """

    cursor = conn.cursor()
    cursor.execute(query)

    teacher_data = defaultdict(lambda: {"subjects": set(), "classes": set(), "teacher_id": None})

    for row in cursor.fetchall():
        teacher_id = row["teacher_id"]
        teacher_name = row["teacher_name"]
        subject_name = row["subject_name"]
        class_name = row["class_name"]

        if teacher_name not in teacher_data:
            teacher_data[teacher_name]["teacher_id"] = teacher_id
        if subject_name:
            teacher_data[teacher_name]["subjects"].add(subject_name)
        if class_name:
            teacher_data[teacher_name]["classes"].add(class_name)

    # Ensure all teachers are included, even those without subjects or classes
    for teacher in cursor.execute("SELECT teacher_id, full_name FROM teachers"):
        teacher_id = teacher["teacher_id"]
        teacher_name = teacher["full_name"]
        if teacher_name not in teacher_data:
            teacher_data[teacher_name] = {"teacher_id": teacher_id, "subjects": set(), "classes": set()}

    # Convert sets to lists for final output
    result = [
        {
            "teacher_id": data["teacher_id"],
            "name": name,
            "subjects": list(data["subjects"]),
            "classes": list(data["classes"])
        }
        for name, data in teacher_data.items()
    ]

    cursor.close()
    conn.close()

    return result


def update_student_info(student_id, student_name, new_data):
    """
    Updates the student information in the database for the given student_id.

    Args:
        student_id (int): The ID of the student to update.
        new_data (dict): A dictionary containing the new field values to update.
        db_path (str): Path to the SQLite database file.
    """
    try:
        # Fetch current student data
        current_data_dict = get_student_details(student_id)
        if not current_data_dict:
            return

            #changes
        changes = {}
        changes_str = ""
        for column, new_value in new_data.items():
            current_value = current_data_dict.get(column)
            if current_value != new_value:
                changes[column] = new_value
                changes_str += f"{column}:'{current_value}''{new_value}'\n"

        if not changes:
            return

        # Construct the UPDATE query
        query = "UPDATE students SET "
        query += ", ".join(f"{col} = ?" for col in changes.keys())
        query += " WHERE student_id = ?"

        # Execute the query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, (*changes.values(), student_id))
        conn.commit()
        activity_type = "update"
        affected_entity = "student"
        entity_name = student_name
        entity_id = student_id
        additional_info = changes_str
        log_activity(
            activity_type,
            affected_entity,
            entity_name,
            entity_id,
            additional_info)
        #return f"Student information updated successfully"  ###########################
        #leaves the connection hanging ?
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        if 'conn' in locals():
            conn.close()





def get_classes_info():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Only returning the calculated [current_students/max_students] string
        query = """
        SELECT class_id, 
               class_name, 
               grade_name, 
               session, 
               creation_data, 
               '' || current_students || '/' || max_students || '' AS students_ratio
        FROM class_view
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        connection.close()
        return rows

    except sqlite3.Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"



## look up teacher (change info)
    ##add subject /remove
    ##

## look up student (change info)
    ## add  /remove class

 ## look up class
    ## add /remove couses
    ##