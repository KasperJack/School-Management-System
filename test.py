import sqlite3

def create_table_and_add_users():
    # Connect to the SQLite database (this will create the database file if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the 'users' table (if it doesn't already exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')

    # Insert some test users into the 'users' table
    users = [
        ('John Doe', 'john.doe@example.com', 'password123', 'admin', 'active'),
        ('Jane Smith', 'jane.smith@example.com', 'password456', 'superadmin', 'active'),
        ('Alice Johnson', 'alice.johnson@example.com', 'password789', 'user', 'inactive'),
        ('Bob Brown', 'bob.brown@example.com', 'password321', 'user', 'active')
    ]

    # Insert the users into the table
    cursor.executemany('''
    INSERT INTO users (name, email, password, type, status) 
    VALUES (?, ?, ?, ?, ?)
    ''', users)

    # Commit the changes and close the connection
    conn.commit()

    print("Table created and users added successfully!")

    # Close the connection
    conn.close()

# Run the function to create the table and insert sample users
create_table_and_add_users()

