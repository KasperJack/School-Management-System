from PyQt6.QtWidgets import QDialog, QMessageBox, QFileDialog,QVBoxLayout,QWidget,QRadioButton,QPushButton,QButtonGroup
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

        self.load_classes()











    def clear_fields(self):
        self.name_field.clear()
        self.last_name_field.clear()
        self.phone_field.clear()
        self.email_field.clear()
        self.address_field.clear()

        self.m_radioButton.setAutoExclusive(False)
        self.f_radioButton.setAutoExclusive(False)


        self.m_radioButton.setChecked(False)
        self.f_radioButton.setChecked(False)

        self.m_radioButton.setAutoExclusive(True)
        self.f_radioButton.setAutoExclusive(True)



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



    def update(self):
        self.clear_fields()
        self.index_instance.load_students_to_table()
        self.index_instance.update_students_count()
        self.index_instance.refresh_setup_activity_log__table()







    
    def add_student(self):

        name = self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        birth_date = self.birth_date.date().toString("dd-MM-yyyy")
        address = self.address_field.text()

        #stdclass = self.classes_dropdown.currentText()
        #class_id = self.classes_dropdown.currentData()


        self.get_selected_class_id()

        if self.m_radioButton.isChecked():
            gender = "M"
        elif self.f_radioButton.isChecked():
            gender = "F"

        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return






        if not name or not last_name or not phone or not email or not address:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        if self.image_bin:
            if stdclass == "N/A":
                evaluate = database.add_student(full_name, phone, email, gender, birth_date, address, photo=self.image_bin)
                if evaluate == "Student added successfully":
                    QMessageBox.information(self, "info", f"{evaluate}")
                    self.update()

                    return
                else:
                    QMessageBox.warning(self, "Error", f"{evaluate}")
                    return

            evaluate = database.add_student(full_name, phone, email, gender, birth_date, address, class_id, self.image_bin)
            if evaluate == "Student added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.update()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")



        if stdclass == "N/A":
            evaluate = database.add_student(full_name,phone,email,gender,birth_date,address)
            if evaluate == "Student added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.update()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return

        evaluate = database.add_student(full_name, phone, email, gender, birth_date,address,class_id)
        if evaluate == "Student added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.update()
            return
        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")




    def get_selected_class_id(self):
        selected_button = self.button_group.checkedButton()

        if selected_button:
            class_id = self.button_group.id(selected_button)
            return class_id
        else:
            return "N/A"





    def load_classes(self):

                classes = classes = database.get_classes_ids()


                #self.scrollArea_class.setWidgetResizable(True)  # Allow the widget to resize

                # Create a container widget for the radio buttons
                self.radio_container = QWidget()
                self.radio_layout = QVBoxLayout(self.radio_container)

                # Add radio buttons for each class
                self.button_group = QButtonGroup()  # To manage radio buttons
                for class_id, class_name in classes:
                    radio_button = QRadioButton(class_name)  # Display class name
                    self.button_group.addButton(radio_button, class_id)  # Associate class ID with the button
                    self.radio_layout.addWidget(radio_button)

                # Set the container widget as the content of the scroll area
                self.scrollArea_class.setWidget(self.radio_container)



                # Create a button to get the selected class ID
                #self.get_selection_button = QPushButton("Get Selected Class ID")
                #self.get_selection_button.clicked.connect(self.get_selected_class_id)



