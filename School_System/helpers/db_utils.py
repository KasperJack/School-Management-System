
import sqlite3
from School_System.db import DB_PATH
from datetime import datetime

LOGGED_IN_USER_NAME = None
LOGGED_IN_USER_ID = None



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


def add_course(teacher_subject,class_name):
    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        try:
            # Insert the data into the teachers_subjects table
            cursor.execute(
                "INSERT INTO course (id, class_name) VALUES (?, ?)",
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




def add_class(class_name, grade_name):
    """
    Insert a new class with the given class_name and grade_name into the class table.
    """


    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        try:
            # Insert the new class into the class table
            cursor.execute(
                "INSERT INTO class (class_name, grade_name) VALUES (?, ?)",
                (class_name, grade_name)
            )
            db_connection.commit()
            db_connection.commit()
            activity_type = "add"
            affected_entity = "class"
            entity_name = class_name
            entity_id = 0
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


















def get_classes():
    """Fetch a list of class names from the database."""


    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        # Query to fetch all class names
        cursor.execute("SELECT class_name FROM class")
        classes = cursor.fetchall()
        classes = [class_name[0] for class_name in classes]

    return classes





def add_student(full_name, phone, email, gender, birth_date, address, class_name=None):
    """
    Inserts a new student into the `students` table and handles integrity errors.
    """
    try:
        with sqlite3.connect(DB_PATH) as db_connection:
            cursor = db_connection.cursor()


            cursor.execute(
                """
                INSERT INTO students (full_name, phone, email, gender, birth_date, address, class_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (full_name, phone, email, gender, birth_date, address, class_name)
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
        # Query to get student info along with grade
        query = """
        SELECT 
            students.student_id,
            students.full_name,
            grades.grade_name,
            students.class_name,
            students.birth_date,
            students.address,
            students.phone,
            students.email
        FROM 
            students
        LEFT JOIN 
            class ON students.class_name = class.class_name
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
            SELECT ts.id, sub.subject_name, t.full_name
            FROM teachers_subjects ts
            JOIN subjects sub ON ts.subject_id = sub.subject_id
            JOIN teachers t ON ts.teacher_id = t.teacher_id
        """)
        teachers_subjects = cursor.fetchall()
        return  teachers_subjects




def get_student_details(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        query = """
        SELECT photo, full_name, phone, email, birth_date, address, class_name, 
               registration_date, additional_info
        FROM students
        WHERE student_id = ?;
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
                "class_name": result[6],
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
    try:
        # Use the existing connection if provided, otherwise create a new one
        if conn is None:
            conn = sqlite3.connect(DB_PATH)

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

        # Commit only if using a new connection
        if conn is not conn:
            conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred in log_activity: {e}")

    finally:
        # Close the connection only if it was created in this function
        if conn is not conn:
            conn.close()




def get_activity_log():

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        #excluding the "additional_info"
        query = """
        SELECT log_id, timestamp, user_id, user_name, 
               activity_type, affected_entity, entity_name, entity_id 
        FROM activity_log
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