import os 
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic

from School_System.helpers.db_utils import get_classes


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddStudentDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Student")

        self.add_student_button.clicked.connect(self.add_student)
        classes = get_classes()
        self.classes_dropdown.addItems(classes)





    
    def add_student(self):

        name = self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        gender = self.comboBox.currentText()
        address = self.address_field.text()





        

