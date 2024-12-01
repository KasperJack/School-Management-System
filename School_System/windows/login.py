import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic

from School_System.windows.CreateAccount import CreateAccountDialog
from School_System.windows.indexSU import indexSU
from School_System.helpers.db_utils import *



class Login(QMainWindow):  
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'login.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Login")
        self.login_button.clicked.connect(self.authenticate_user)
        self.create_account_button.clicked.connect(self.create_account)
        self.forget_password_button.clicked.connect(self.forget_password)
        self.view_password_button.clicked.connect(self.toggle_password_visibility)
        self.remember_me_button.toggled.connect(self.remember_me)


    def remember_me(self, checked):
        if checked:
            self.email_field.setText("Button is checked")
        else:
            self.email_field.setText("Button is unchecked")



    def forget_password(self):
        pass



    def create_account(self):
        # Create an instance of the CreateAccountDialog
        create_account_dialog = CreateAccountDialog(self)  
        create_account_dialog.exec()  






    def toggle_password_visibility(self):
        # Toggle the echoMode of the password field
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)




        

    def authenticate_user(self):
        # Get email and password from input fields
        email = self.email_field.text()
        password = self.password_field.text()

        # Validate inputs
        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Both email and password fields must be filled.")
            return
        
        evaluate, name = login_user(email,password)

        if evaluate == SUPERADMIN:
            QMessageBox.information(self, "superadmin",f"Welcome {name}")
            # Load the IndexSU window
            self.index_window = indexSU()  
            self.index_window.show()   
            self.close()    



        elif evaluate == ADMIN:
            QMessageBox.information(self, " admin",f"Welcome {name}")


        elif evaluate == USER_INACTIVE:
            QMessageBox.critical(self, "Login Failed", f"Your account {name} is inactive .")

        else:
            QMessageBox.critical(self, "Login Failed", "Invalid email or password. Please try again.")




##=========================================================##
##
##END ##
##
##=========================================================##        



        
            

    




