import os

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from School_System.helpers.db_utils import *



class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddClassDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Class")

        self.add_class_button.clicked.connect(self.add_class)





    
    
    
    
    def add_class(self):


        # Get info from input fields
        subject_name = self.subject_name_field.text()
        description = self.description_field.text()

        # Validate input fields
        if not subject_name:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        if not description:
            evaluate = add_subject(subject_name)
            if evaluate == "Subject added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.subject_name_field.clear()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return



        evaluate = add_subject(subject_name,description)

        if evaluate == "Subject added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.subject_name_field.clear()
            self.description_field.clear()
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")




        

