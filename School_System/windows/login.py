from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic

from School_System.ui import LOGIN # ui file path
from School_System.windows.CreateAccountDialog import CreateAccountDialog
from School_System.windows.IndexSU import IndexSU
import School_System.helpers.db_utils as database



class Login(QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi(LOGIN, self)

        self.setWindowTitle("Login")
        self.login_button.clicked.connect(self.authenticate_user)
        self.create_account_button.clicked.connect(self.open_create_account_dialog)
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



    def open_create_account_dialog(self):
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
        
        evaluate = database.login_user(email,password)

        if evaluate == database.SUPERADMIN:
            QMessageBox.information(self, "superadmin",f"Welcome {database.LOGGED_IN_USER_NAME}")
            # Load the IndexSU window
            self.index_window = IndexSU()
            self.index_window.show()   
            self.close()    



        elif evaluate == database.ADMIN:
            QMessageBox.information(self, " admin",f"Welcome {database.LOGGED_IN_USER_NAME}")
            # Load the IndexSU window(for admins)
            self.index_window = IndexSU()
            self.index_window.show()
            self.close()


        elif evaluate == database.USER_INACTIVE:
            QMessageBox.critical(self, "Login Failed", f"account {name} is inactive .")

        else:
            QMessageBox.critical(self, "Login Failed", "Invalid email or password. Please try again.")




##=========================================================##
##
##END ##
##
##=========================================================##        



        
            

    




