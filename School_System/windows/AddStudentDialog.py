from PyQt6.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import ADD_STUDENT_DIALOG
#from School_System.windows.indexSU import indexSU this is  causes an infinite loop  ,Passing index_instance allows the dialog to access the indexSU

class AddStudentDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(ADD_STUDENT_DIALOG, self)

        self.setWindowTitle("Add Student")

        self.add_student_button.clicked.connect(self.add_student)
        self.add_pic.clicked.connect(self.open_image_dialog)

        self.classes_dropdown.addItem("N/A")
        self.image_bin = None


        classes = database.get_classes_ids()
        for class_id, class_name in classes:
            self.classes_dropdown.addItem(class_name, class_id)

        self.classes_dropdown.setCurrentIndex(0)


    def clear_fields(self):
        self.name_field.clear()
        self.last_name_field.clear()
        self.phone_field.clear()
        self.email_field.clear()
        self.address_field.clear()



    def open_image_dialog(self):
        # Open the file dialog
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",  # Starting directory
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"  # File filter
        )

        # Validate the file type
        if image_path and image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            with open(image_path, "rb") as file:
                binary_data = file.read()
            self.image_bin = binary_data


        else:
            self.image_bin = None

















    
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
        class_id = self.classes_dropdown.currentData()


        if not name or not last_name or not phone or not email or not address:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        if self.image_bin:
            if stdclass == "N/A":
                evaluate = database.add_student(full_name, phone, email, gender, birth_date, address)
                if evaluate == "Student added successfully":
                    QMessageBox.information(self, "info", f"{evaluate}")
                    self.clear_fields()
                    self.index_instance.load_students_to_table()
                    self.index_instance.update_students_count()
                    self.index_instance.refresh_setup_activity_log__table()
                    return
                else:
                    QMessageBox.warning(self, "Error", f"{evaluate}")
                    return

            evaluate = database.add_student(full_name, phone, email, gender, birth_date, address, class_id)
            if evaluate == "Student added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.clear_fields()
                self.index_instance.load_students_to_table()
                self.index_instance.update_students_count()
                self.index_instance.refresh_setup_activity_log__table()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")



        if stdclass == "N/A":
            evaluate = database.add_student(full_name,phone,email,gender,birth_date,address)
            if evaluate == "Student added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.clear_fields()
                self.index_instance.load_students_to_table()
                self.index_instance.update_students_count()
                self.index_instance.refresh_setup_activity_log__table()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return

        evaluate = database.add_student(full_name, phone, email, gender, birth_date,address,class_id)
        if evaluate == "Student added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.clear_fields()
            self.index_instance.load_students_to_table()
            self.index_instance.update_students_count()
            self.index_instance.refresh_setup_activity_log__table()
            return
        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")







        

