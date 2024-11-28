import os

def connect():
    # Get the absolute path to the database file in the 'db' directory
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'school.db')
    
    # Check if the database exists (optional, for validation)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    
    return db_path


