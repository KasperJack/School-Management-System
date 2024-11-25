import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("app_users.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL command to create the 'users' table
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    users_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT NOT NULL
);
"""

# Execute the SQL command
cursor.execute(create_users_table)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Users table created successfully!")

