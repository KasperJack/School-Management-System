
import sqlite3
from School_System.db.dbio import connect

# Define constants for return values
SUPERADMIN = "superadmin"
ADMIN = "admin"
USER_INACTIVE = "inactive"
INVALID_CREDENTIALS = "invalid"

def login_user(email, password):
    # Connect to the database
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
            user_type = result[4]  # User type column

            if status == 'inactive':  # Explicitly check for inactive users
                return USER_INACTIVE

            if status == 'active':
                if user_type == 'superadmin':
                    return SUPERADMIN
                elif user_type == 'admin':
                    return ADMIN

        return INVALID_CREDENTIALS  # If no match is found


