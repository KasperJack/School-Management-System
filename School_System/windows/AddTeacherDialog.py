import os

from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox, QCheckBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6 import uic
from School_System.helpers.db_utils import *

import sqlite3
from School_System.db.dbio import connect

class AddTeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddTeacherDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Teacher")

        self.add_teacher_button.clicked.connect(self.add_teacher)
        self.load_subjects()



    def load_subjects(self):
        """Fetch subjects from the database and populate the subjects_widget with checkboxes."""
        db_path = connect()
        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()

            # Fetch all subjects from the 'subject' table
            cursor.execute("SELECT subject_name FROM subject")
            subjects = cursor.fetchall()

        # Ensure the widget has a layout
        if self.subjects_widget.layout() is None:
            self.subjects_widget.setLayout(QVBoxLayout())  # Use QVBoxLayout if none exists

        # Clear the existing layout
        while self.subjects_widget.layout().count():
            child = self.subjects_widget.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Populate the subjects_widget with checkboxes
        for subject_name in subjects:
            # Create a horizontal layout for each subject
            row_layout = QHBoxLayout()

            # Create a label for the subject name
            subject_label = QLabel(subject_name[0], self)  # Use subject_name[0] as fetchall returns a tuple

            # Create a checkbox for selection
            subject_checkbox = QCheckBox(self)
            subject_checkbox.setObjectName(f"checkbox_{subject_name[0]}")  # Use subject name for identification

            # Add the label and checkbox to the horizontal layout
            row_layout.addWidget(subject_label)
            row_layout.addWidget(subject_checkbox)

            # Add the horizontal layout to the main layout of subjects_widget
            self.subjects_widget.layout().addLayout(row_layout)

    def save_selected_subjects(self, teacher_full_name):
        """Save the selected subjects for a teacher to the database."""
        db_path = connect()
        selected_subjects = []

        # Retrieve selected subjects from the widget
        layout = self.subjects_widget.layout()
        for i in range(layout.count()):
            row_layout = layout.itemAt(i)
            if isinstance(row_layout, QHBoxLayout):
                checkbox = row_layout.itemAt(1).widget()  # Checkbox is the second widget
                if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                    # Get the subject name from the checkbox object name
                    subject_name = row_layout.itemAt(0).widget().text()  # Text of the label
                    selected_subjects.append(subject_name)

        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()

            # Get teacher details
            cursor.execute("SELECT full_name FROM teachers WHERE full_name = ?", (teacher_full_name,))
            teacher = cursor.fetchone()
            if not teacher:
                print(f"Teacher '{teacher_full_name}' not found.")
                return False

            # Insert selected subjects into the teachers_subjects table
            for subject_name in selected_subjects:
                cursor.execute(
                    "INSERT INTO teachers_subjects (full_name, subject_name) VALUES (?, ?)",
                    (teacher_full_name, subject_name)
                )
            db_connection.commit()

        print(f"Successfully saved subjects for teacher: {teacher_full_name}")
        return True



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
            #selected_subjects = self.get_selected_subjects()
            if evaluate == "Teacher added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.name_field.clear()
                self.last_name_field.clear()
                self.phone_field.clear()
                self.email_field.clear()
                self.save_selected_subjects(full_name)
                #for subject_id in selected_subjects:
                    #add_teacher_subject(email,subject_id)
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return


        evaluate = add_teacher(full_name, phone, email,gender,address)
        if evaluate == "Teacher added successfully":
            #selected_subjects = self.get_selected_subjects()
            QMessageBox.information(self, "info", f"{evaluate}")
            self.name_field.clear()
            self.last_name_field.clear()
            self.phone_field.clear()
            self.email_field.clear()
            self.address_field.clear()
            self.save_selected_subjects(full_name)
            #for subject_id in selected_subjects:
                #add_teacher_subject(email, subject_id)
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")


        

