from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sqlite3



class CreateAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('CreateAccount.ui', self)

        self.setWindowTitle("Create Account")

        self.create_account_button.clicked.connect(self.create_account)





    
    
    
    
    def create_account(self):
        # Connect to the database
        self.db_connection = sqlite3.connect('school.db')
        self.cursor = self.db_connection.cursor()

        # Get info from input fields
        full_name = self.full_name_field.text()
        email = self.email_field.text()
        pass1 = self.pass1_field.text()
        pass2 = self.pass2_field.text()

        # Validate input fields
        if not full_name or not email or not pass1:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        if pass1 != pass2:
            QMessageBox.warning(self, "Password Mismatch", "Passwords do not match.")
            return

        try:
            # Insert user into the database
            query = """
                INSERT INTO users (full_name, email, password) 
                VALUES (?, ?, ?)
            """
            self.cursor.execute(query, (full_name, email, pass1))
            self.db_connection.commit()

            QMessageBox.information(self, "Success", "Account created successfully!")
            self.close()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

        finally:
            self.db_connection.close()
