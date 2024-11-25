import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic
import sqlite3



class Login(QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)  # Load the .ui file

        self.setWindowTitle("Login")

        # Connect the login button to the login method
        self.login_button.clicked.connect(self.authenticate_user)
        self.view_password.clicked.connect(self.toggle_password_visibility)



    def toggle_password_visibility(self):
        # Toggle the echoMode of the password field
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)




    def authenticate_user(self):
        # Connect to the database ##################
        self.db_connection = sqlite3.connect('users.db')
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
            status = result[5]  # Assuming status is the 5th column in the result (index 4)
            user_type = result[4]  # Assuming type is the 4th column in the result (index 3)

            # Combine the login logic with the status and user type checks
            if status == 'active' and (user_type == 'admin' or user_type == 'superadmin'):
                # If the user is active and of the correct type, show success message
                QMessageBox.information(self, "Login Successful", f"Welcome, {result[1]}!")
            else:
                # If the status is not 'active' or the type is not 'admin' or 'superadmin'
                QMessageBox.critical(self, "Login Failed", "Your account is either inactive or does not have the correct permissions.")
        else:
            # If credentials are invalid, display error message
            QMessageBox.critical(self, "Login Failed", "Invalid email or password. Please try again.")

        # Close the database connection after the authentication check
        self.db_connection.close()
            

    









# Entry point of the program
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Login()  # Create an instance of the Login class
    window.show()  # Show the window

    sys.exit(app.exec())  # Execute the application
