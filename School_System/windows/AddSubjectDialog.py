import os 
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from School_System.helpers.db_utils import *



class AddSubjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddSubjectDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Subject")

        self.add_subject_button.clicked.connect(self.add_subject)





    
    
    
    
    def add_subject(self):


        # Get info from input fields
        subject = self.subject_name_field
        description = self.description_field

        # Validate input fields
        if not subject:
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

        




        

