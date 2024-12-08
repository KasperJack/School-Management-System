import os 
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic

from School_System.helpers.db_utils import get_classes, add_student


class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddStudentDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Student")

        self.add_student_button.clicked.connect(self.add_student)
        self.classes_dropdown.addItem("N/A")
        classes = get_classes()
        self.classes_dropdown.addItems(classes)

        self.classes_dropdown.setCurrentIndex(0)



    
    def add_student(self):

        name = self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        gender = self.comboBox.currentText()
        birth_date = self.birth_date.date().toString("dd-MM-yyyy")
        stdclass = self.classes_dropdown.currentText()

        if not name or not last_name or not phone or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        if stdclass == "N/A":
            evaluate = add_student(full_name,phone,email,gender,birth_date)
            if evaluate == "Student added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.name_field.clear()
                self.last_name_field.clear()
                self.phone_field.clear()
                self.email_field.clear()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return

        evaluate = add_student(full_name, phone, email, gender, birth_date,stdclass)
        if evaluate == "Student added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.name_field.clear()
            self.last_name_field.clear()
            self.phone_field.clear()
            self.email_field.clear()
            return
        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")





        

