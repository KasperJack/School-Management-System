import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic
import sqlite3
from School_System.windows.CreateAccount import CreateAccountDialog
from School_System.windows.indexSU import indexSU
from School_System.db.dbio import connect


class Login(QMainWindow):  
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'login.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Login")

        self.login_button.clicked.connect(self.authenticate_user)

        self.create_account_button.clicked.connect(self.create_account)
        self.forget_password_button.clicked.connect(self.forget_password)







    def forget_password(self):
        pass



    def create_account(self):
        # Create an instance of the CreateAccountDialog
        create_account_dialog = CreateAccountDialog(self)  # Pass self as parent
        create_account_dialog.exec()  # Open the dialog modally





    def toggle_password_visibility(self):
        # Toggle the echoMode of the password field
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)




    def authenticate_user(self):
        # Connect to the database ##################
        db = connect()
        self.db_connection = sqlite3.connect(db)
        self.cursor = self.db_connection.cursor()

        # Get email and password from input fields
        email = self.email_field.text()
        password = self.password_field.text()

        # Validate inputs
        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Both email and password fields must be filled.")
            return

        # Query the database to check for user credentials
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        self.cursor.execute(query, (email, password))
        result = self.cursor.fetchone()

        if result:
            # Check if the user is active and has the correct type (admin or superadmin)
            status = result[5]  
            user_type = result[4]  
            #print(status)
            #print(user_type)

            # Combine the login logic with the status and user type checks
            if status == 'active' and (user_type == 'superadmin'):
                # If the user is active and of the correct type, show success message
                QMessageBox.information(self, "As sudo", f"Welcome, {result[1]}!")
                # Load the Index window
                self.index_window = indexSU()  # Initialize the main window
                self.index_window.show()    # Show the main window
                self.close() 





            elif status == 'active' and (user_type == 'admin'):
                QMessageBox.information(self, "as Admin", f"Welcome, {result[1]}!")

            else:
                # If the status is not 'active' or the type is not 'admin' or 'superadmin'
                QMessageBox.critical(self, "Login Failed", "Your account is inactive .")
        else:
            # If credentials are invalid, display error message
            QMessageBox.critical(self, "Login Failed", "Invalid email or password. Please try again.")

        # Close the database connection after the authentication check
        self.db_connection.close()
            

    




