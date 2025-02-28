import os
import shutil
import json
from School_System.conf import SCHEMA
from School_System.conf import SETTINGS




class DatabaseManager:
    def __init__(self):
        if not hasattr(self, 'initialized'):

            self.initialized = True
            self.DB_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
            self.SCHEMA_FILE = SCHEMA
            self.METADATA_FILE = SETTINGS

            self.metadata = self._load_metadata()
            self.current_db = self.metadata.get("current_db")
            self.current_db_path = f"{self.DB_DIRECTORY}/{self.current_db}"
            #print(self.current_db)
            #print(self.current_db_path)


    def reset(self):
        self.metadata = self._load_metadata()
        self.current_db = self.metadata.get("current_db")
        self.current_db_path = f"{self.DB_DIRECTORY}/{self.current_db}"


    def _load_metadata(self):
        """Load the metadata from the configuration file."""
        metadata_path = SETTINGS
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                return json.load(f)
        else:
            return {}





    def change_database(self,db_name):
        if os.path.exists(SETTINGS):
            try:
                with open(SETTINGS, "r") as f:
                    settings = json.load(f)

                settings['current_db'] = db_name

                with open(SETTINGS, "w") as f:
                    json.dump(settings, f, indent=4)
                self.reset()

            except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
                print(f"Error setting 'remember' to True: {e}")


    def create_new_db(self, new_db_name):
        """Create a new DB by copying the schema file and update metadata."""
        # Ensure the new DB name has a .db extension
        if not new_db_name.endswith(".db"):
            new_db_name += ".db"

        new_db_path = os.path.join(self.DB_DIRECTORY, new_db_name)

        # Copy the schema file to the new database file
        schema_path = os.path.join(self.DB_DIRECTORY, self.SCHEMA_FILE)
        if os.path.exists(schema_path):
            shutil.copy(schema_path, new_db_path)
            # Update the metadata with the new database
            self.last_db = self.current_db
            self.current_db = new_db_path
            self._save_metadata()  # Save the metadata file
        else:
            print(f"Schema file '{self.SCHEMA_FILE}' not found.")



  ## retruns an arry with no mark in the case of false
    def get_all_databases(self):
        """Return a list of all .db files in the DB_DIRECTORY, indicating the current one."""
        db_files = [
            f for f in os.listdir(self.DB_DIRECTORY) if f.endswith(".db")
        ]

        # Mark the current database
        db_files_with_status = [
            f"{db} (current)" if db == self.current_db else db for db in db_files
        ]

        return db_files_with_status








db_manager_instance = DatabaseManager()