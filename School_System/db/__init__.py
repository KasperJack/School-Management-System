import os

DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")

import sqlite3
import os
import shutil
import json


class DatabaseManager:
    DB_DIRECTORY = "db_files"  # Directory to store DBs
    SCHEMA_FILE = "schema.db"  # The base schema file
    METADATA_FILE = "db_metadata.json"  # To track last and current DB

    def __init__(self):
        """Initialize the manager and load metadata."""
        #os.makedirs(self.DB_DIRECTORY, exist_ok=True)
        self.metadata = self._load_metadata()
        self.current_db = self.metadata.get("current_db")
        self.last_db = self.metadata.get("last_db")


    def _load_metadata(self):
        """Load or create metadata for tracking databases."""
        if os.path.exists(self.METADATA_FILE):
            with open(self.METADATA_FILE, "r") as f:
                return json.load(f)
        return {"current_db": None, "last_db": None}



    def _save_metadata(self):
        """Save metadata to track the last and current DB."""
        with open(self.METADATA_FILE, "w") as f:
            json.dump(self.metadata, f)


    def create_database(self, db_name):
        """Create a new database by copying the schema file."""
        new_db_path = os.path.join(self.DB_DIRECTORY, f"{db_name}.db")

        if os.path.exists(new_db_path):
            print(f"Database {db_name} already exists!")
            return

        if not os.path.exists(self.SCHEMA_FILE):
            print("Schema file not found! Cannot create database.")
            return

        shutil.copy(self.SCHEMA_FILE, new_db_path)
        self.set_database(db_name)  # Switch to the new DB
        print(f"Database {db_name} created and set as active.")

    def list_databases(self):
        """Return a list of all database files in the directory."""
        return [f for f in os.listdir(self.DB_DIRECTORY) if f.endswith(".db")]

    def set_database(self, db_name):
        """Set a database as the current active one."""
        db_path = os.path.join(self.DB_DIRECTORY, f"{db_name}.db")

        if not os.path.exists(db_path):
            print(f"Database {db_name} does not exist!")
            return

        self.metadata["last_db"] = self.current_db
        self.metadata["current_db"] = db_path
        self._save_metadata()
        self.current_db = db_path
        print(f"Switched to database: {db_name}")


    def get_current_db(self):
        """Get the current active database path."""
        return self.current_db


    def get_last_db(self):
        """Get the last used database path."""
        return self.last_db

    def connect(self):
        """Connect to the current database."""
        if not self.current_db:
            print("No database selected!")
            return None
        return sqlite3.connect(self.current_db)





