import os

from PyQt6.QtWidgets import QDialog, QMessageBox,QComboBox
from PyQt6 import uic
from School_System.helpers.db_utils import *



class AddTeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddTeacherDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Teacher")

        self.add_teacher_button.clicked.connect(self.add_teacher)


    def add_teacher(self):
        name =self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        gender = self.comboBox.currentText()
        address = self.address_field.text()

        if not name or not last_name or not email or not phone or not gender:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        if not address:
            evaluate = add_teacher(full_name,phone,email,gender)
            if evaluate == "Teacher added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.name_field.clear()
                self.last_name_field.clear()
                self.phone_field.clear()
                self.email_field.clear()
               #self.comboBox.clear()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return


        evaluate = add_teacher(full_name, phone, email,gender,address)
        if evaluate == "Teacher added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.name_field.clear()
            self.last_name_field.clear()
            self.phone_field.clear()
            self.email_field.clear()
            self.address_field.clear()
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")


        

