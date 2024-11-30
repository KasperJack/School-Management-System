
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
            if status == 'inactive':  # explicitly check for inactive users
                return USER_INACTIVE, name
            if status == 'active':
                if user_type == 'superadmin':
                    return SUPERADMIN, name
                elif user_type == 'admin':
                    return ADMIN, name

        return INVALID_CREDENTIALS, None  # gitaddno match is found






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
        return f"An error occurred: {e}"


