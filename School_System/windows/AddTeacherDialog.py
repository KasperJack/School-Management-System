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
            cursor.execute("SELECT subject_id, subject_name FROM subject")
            subjects = cursor.fetchall()

        # Ensure the widget has a layout
        if self.subjects_widget.layout() is None:
            self.subjects_widget.setLayout(QVBoxLayout())  # QVBoxLayout if none exists

        # Clear the layout
        while self.subjects_widget.layout().count():
            child = self.subjects_widget.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Populate the subjects_widget with checkboxes
        for subject_id, subject_name in subjects:
            # Create a horizontal layout for each subject
            row_layout = QHBoxLayout()

            # Create a label for the subject name
            subject_label = QLabel(subject_name, self)

            # Create a checkbox for selection
            subject_checkbox = QCheckBox(self)
            subject_checkbox.setObjectName(f"checkbox_{subject_id}")  # Optional: Unique identifier

            # Add the label and checkbox to the horizontal layout
            row_layout.addWidget(subject_label)
            row_layout.addWidget(subject_checkbox)

            # Add the horizontal layout to the main layout of subjects_widget
            self.subjects_widget.layout().addLayout(row_layout)




    def loadd_subjects(self):
        """Fetch subjects from the database and populate the dropdown."""
        db_path = connect()  # Assuming `connect()` returns the database file path
        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT subject_name FROM subject")
            subjects = cursor.fetchall()

        # Add subjects to the dropdown
        for subject_name, in subjects:  # Use single-element unpacking
            self.subject_dropdown.addItem(subject_name)



    def get_selected_subjects(self):
        """Get a list of selected subject IDs."""
        selected_subjects = []  # Store the IDs of selected subjects
        layout = self.subjects_widget.layout()

        # Iterate through the rows in the layout
        for i in range(layout.count()):
            row_layout = layout.itemAt(i)  # Get the row's layout
            if isinstance(row_layout, QHBoxLayout):
                # Get the checkbox (second widget in the row layout)
                checkbox = row_layout.itemAt(1).widget()
                if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                    # Extract the subject ID from the checkbox's object name
                    subject_id = int(checkbox.objectName().split('_')[-1])
                    selected_subjects.append(subject_id)

        return selected_subjects





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
            selected_subjects = self.get_selected_subjects()
            if evaluate == "Teacher added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.name_field.clear()
                self.last_name_field.clear()
                self.phone_field.clear()
                self.email_field.clear()
                for subject_id in selected_subjects:
                    add_teacher_subject(email,subject_id)
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return


        evaluate = add_teacher(full_name, phone, email,gender,address)
        if evaluate == "Teacher added successfully":
            selected_subjects = self.get_selected_subjects()
            QMessageBox.information(self, "info", f"{evaluate}")
            self.name_field.clear()
            self.last_name_field.clear()
            self.phone_field.clear()
            self.email_field.clear()
            self.address_field.clear()
            for subject_id in selected_subjects:
                add_teacher_subject(email, subject_id)
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")


        

