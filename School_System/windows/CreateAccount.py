import os 
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from School_System.helpers.db_utils import add_account_user



class CreateAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'CreateAccount.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Create Account")

        self.create_account_button.clicked.connect(self.create_account)





    
    
    
    
    def create_account(self):


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

     
        evaluate = add_account_user(full_name,email,pass1)

        if evaluate == 'This email already exists':
            QMessageBox.warning(self, "Error", f"{evaluate}")
            return
        
        else:
            QMessageBox.information(self, "info", f"{evaluate}")
            self.close()

        




        

