import os

from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox, QCheckBox, QHBoxLayout, QLabel, QVBoxLayout ,QGridLayout
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
        """Fetch subjects from the database and populate the subjects_scrollArea with checkboxes."""
        db_path = connect()
        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute("SELECT subject_name FROM subject")
            subjects = cursor.fetchall()

        # Access or create the scroll area widget
        scroll_widget = self.subjects_scrollArea.widget()
        if scroll_widget is None:
            scroll_widget = QWidget()
            self.subjects_scrollArea.setWidget(scroll_widget)
            self.subjects_scrollArea.setWidgetResizable(True)

        # Set up a layout if not already present
        if scroll_widget.layout() is None:
            scroll_widget.setLayout(QVBoxLayout())

        layout = scroll_widget.layout()

        # Clear existing widgets in the layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add checkboxes for each subject
        for subject_name in subjects:
            checkbox = QCheckBox(subject_name[0], self)
            checkbox.setObjectName(f"checkbox_{subject_name[0]}")
            layout.addWidget(checkbox)



    def get_selected_subjects(self):
        """Retrieve selected subjects from the scroll area."""
        selected_subjects = []

        # Access the widget inside the scroll area
        scroll_widget = self.subjects_scrollArea.widget()
        if scroll_widget is None or scroll_widget.layout() is None:
            print("Error: Scroll area does not have a proper widget or layout.")
            return selected_subjects  # Return an empty list if layout is missing

        layout = scroll_widget.layout()

        # Iterate through the items in the layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()

            # Check if the widget is a QCheckBox and is checked
            if isinstance(widget, QCheckBox) and widget.isChecked():
                selected_subjects.append(widget.text())  # Append the checkbox text

        return selected_subjects




    def clear_checkbox_selection(self):
        """Clear all checkbox selections in the subjects_scrollArea."""
        # Access the widget inside the scroll area
        scroll_widget = self.subjects_scrollArea.widget()

        if scroll_widget is None or scroll_widget.layout() is None:
            print("Error: Scroll area does not have a proper widget or layout.")
            return

        layout = scroll_widget.layout()

        # Iterate through the items in the layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()

                # Check if the widget is a QCheckBox and uncheck it
                if isinstance(widget, QCheckBox):
                    widget.setChecked(False)




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
                for subject in selected_subjects:
                    add_teacher_subject(full_name,subject)
                self.clear_checkbox_selection()
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
            for subject in selected_subjects:
                add_teacher_subject(full_name,subject)
            self.clear_checkbox_selection()
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")


        

