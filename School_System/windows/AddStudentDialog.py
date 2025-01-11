from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from School_System.helpers.db_utils import get_classes, add_student
from School_System.ui import ADD_STUDENT_DIALOG
#from School_System.windows.indexSU import indexSU this is  causes an infinite loop  ,Passing index_instance allows the dialog to access the indexSU

class AddStudentDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(ADD_STUDENT_DIALOG, self)

        self.setWindowTitle("Add Student")

        self.add_student_button.clicked.connect(self.add_student)
        self.classes_dropdown.addItem("N/A")
        classes = get_classes()
        self.classes_dropdown.addItems(classes)

        self.classes_dropdown.setCurrentIndex(0)


    def clear_fields(self):
        self.name_field.clear()
        self.last_name_field.clear()
        self.phone_field.clear()
        self.email_field.clear()
        self.address_field.clear()





    
    def add_student(self):

        name = self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        gender = self.comboBox.currentText()
        birth_date = self.birth_date.date().toString("dd-MM-yyyy")
        address = self.address_field.text()
        stdclass = self.classes_dropdown.currentText()

        if not name or not last_name or not phone or not email or not address:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        if stdclass == "N/A":
            evaluate = add_student(full_name,phone,email,gender,birth_date,address)
            if evaluate == "Student added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.clear_fields()
                self.index_instance.load_students_to_table()
                self.index_instance.update_students_count()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return

        evaluate = add_student(full_name, phone, email, gender, birth_date,address,stdclass)
        if evaluate == "Student added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.clear_fields()
            self.index_instance.load_students_to_table()
            self.index_instance.update_students_count()
            return
        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")







        

