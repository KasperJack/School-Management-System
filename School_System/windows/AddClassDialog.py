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
        grades = get_grades()
        self.grades_dropdown.addItems(grades)




    
    
    
    
    def add_class(self):

        #info from input fields
        class_name = self.class_name_field
        grade_name = self.grades_dropdown.currentText()

        # Validate input fields
        if not class_name or not grade_name:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        evaluate = add_class(class_name,grade_name)
        if evaluate == "Subject added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.class_name_field.clear()
            return
        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")






        

