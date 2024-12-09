
import sqlite3
from School_System.db.dbio import connect

# constants for return values
SUPERADMIN = "superadmin"
ADMIN = "admin"
USER_INACTIVE = "inactive"
INVALID_CREDENTIALS = "invalid"


def login_user(email, password):
    ######## connect to the database ########
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()

        # Query the database for the user
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:
            # Extract user details
            status = result[5]  # Status column
            user_type = result[4] # User type column
            name = result[1]
            id = result[0]
            if status == 'inactive':  # explicitly check for inactive users
                return USER_INACTIVE, name
            if status == 'active':
                if user_type == 'superadmin':
                    log_user_in(id)
                    return SUPERADMIN, name
                elif user_type == 'admin':
                    log_user_in(id)
                    return ADMIN, name


        return INVALID_CREDENTIALS, None  # gitaddno match is found




#adds a user to the db (admin)
def add_account_user(full_name, email, password):

    db_path = connect()
    try:
        with sqlite3.connect(db_path) as db_connection:
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
def get_inactive_users():
    # Connect to the database
    db_path = connect()  # Replace with your database connection method
    with sqlite3.connect(db_path) as db_connection:
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
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE full_name = ? AND email = ?", (full_name, email))
        db_connection.commit()






def activate_admin(full_name,email):
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("UPDATE users SET status = 'active' WHERE full_name = ? AND email = ?", (full_name, email))
        db_connection.commit()




#adds admin the entry log
def log_user_in(user_id):
    # Connect to the database
    db_path = connect()  
    with sqlite3.connect(db_path) as db_connection:
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
            # Insert or replace the logged-in user entry
            insert_query = """
                INSERT OR REPLACE INTO logged_in_user (id, full_name, email, type)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_query, user_data)
            db_connection.commit()
        else:
            raise ValueError(f"User with ID {user_id} not found.")




#add the return of the role here
def get_logged_in_user():
    # Connect to the database
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch the last logged-in user
        query = """
            SELECT full_name 
            FROM logged_in_user 
            ORDER BY ROWID DESC 
            LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the full name of the last logged-in user
        else:
            return None  # Return None if no user is logged in





def clear_entry_log():
    # Connect to the database
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
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
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()

        # Insert query to add a new subject
        query = """
            INSERT INTO subjects (subject_name, description) 
            VALUES (?, ?)
        """
        try:
            cursor.execute(query, (subject_name, description))
            db_connection.commit()
            return "Subject added successfully"
        except sqlite3.Error as e:
            return f"{e}"




def add_teacher(full_name, phone, email, gender, address=None):
    try:

        db_path = connect()
        with sqlite3.connect(db_path) as db_connection:
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

        return "Teacher added successfully"

    except sqlite3.IntegrityError as e:
        # Handle unique constraint violations (e.g., duplicate phone or email)
        return f"{e}"

    except sqlite3.Error as e:
        return f"{e}"




def update_teachers_count():
    pass



def add_teacher_subject(teacher_id, subject_id):
    """
    Insert a teacher's subject into the teachers_subjects table.
    """
    db_path = connect()  # Get the database path
    with sqlite3.connect(db_path) as db_connection:
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
    db_path = connect()  # Get the database path
    with sqlite3.connect(db_path) as db_connection:
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
    db_path = connect()

    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT grade_name FROM grades")
        grades = cursor.fetchall()  # Fetch all grade names
        grades = [grade[0] for grade in grades]
    return  grades




def add_class(class_name, grade_name):
    """
    Insert a new class with the given class_name and grade_name into the class table.
    """
    db_path = connect()  # Assuming 'connect()' provides the database path

    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()

        try:
            # Insert the new class into the class table
            cursor.execute(
                "INSERT INTO class (class_name, grade_name) VALUES (?, ?)",
                (class_name, grade_name)
            )
            db_connection.commit()
            return "Class added successfully"
        except sqlite3.IntegrityError as e:
            return f"{e}"




def get_teachers_sequence():
    """
    Fetch the sequence number from the sqlite_sequence table for the 'teachers' table.

    Returns:
        int: The current sequence number for the 'teachers' table, or None if not found.
    """
    db_path = connect()

    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()

        # Query to fetch the sequence number for 'teachers'
        query = "SELECT seq FROM sqlite_sequence WHERE name = 'teachers';"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

    # Return the sequence number if found, else None
    return result[0] if result else None



def get_classes():
    """Fetch a list of class names from the database."""
    db_path = connect()

    with sqlite3.connect(db_path) as db_connection:
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
    db_path = connect()

    try:
        with sqlite3.connect(db_path) as db_connection:
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
            return "Student added successfully"

    except sqlite3.IntegrityError as e:
        #integrity errors ( foreign key violations, unique constraint failures)
        return f"{e}"
    except Exception as e:
        #handle other database errors
        return f"{e}"





## look up teacher (change info)
    ##add subject /remove
    ##

## look up student (change info)
    ## add  /remove class

 ## look up class
    ## add /remove couses
    ##