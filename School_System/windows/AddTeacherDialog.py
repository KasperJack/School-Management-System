

from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox, QCheckBox, QHBoxLayout, QLabel, QVBoxLayout ,QGridLayout
from PyQt6 import uic
from School_System.helpers.db_utils import *
from School_System.ui import ADD_TEACHER_DIALOG # UI FILE


class AddTeacherDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(ADD_TEACHER_DIALOG, self)

        self.setWindowTitle("Add Teacher")

        self.add_teacher_button.clicked.connect(self.add_teacher)
        self.load_subjects()



    def load_subjects(self):

        subjects = get_subjects()

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
        for subject_id, subject_name in subjects:
            checkbox = QCheckBox(subject_name, self)
            checkbox.setObjectName(f"checkbox_{subject_id}")  # Use subject ID in the object name
            checkbox.setProperty("subject_id", subject_id)  # Store subject ID as a property
            layout.addWidget(checkbox)

    def get_selected_subjects(self):
        """Retrieve IDs of selected subjects from the scroll area."""
        selected_subject_ids = []

        # Access the widget inside the scroll area
        scroll_widget = self.subjects_scrollArea.widget()
        if scroll_widget is None or scroll_widget.layout() is None:
            print("Error: Scroll area does not have a proper widget or layout.")
            return selected_subject_ids  # Return an empty list if layout is missing

        layout = scroll_widget.layout()

        # Iterate through the items in the layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()

            # Check if the widget is a QCheckBox and is checked
            if isinstance(widget, QCheckBox) and widget.isChecked():
                # Retrieve the subject ID stored in the checkbox property
                subject_id = widget.property("subject_id")
                if subject_id is not None:
                    selected_subject_ids.append(subject_id)

        return selected_subject_ids



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



    def clear_fields(self):
        self.name_field.clear()
        self.last_name_field.clear()
        self.phone_field.clear()
        self.email_field.clear()
        self.address_field.clear()




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
                self.clear_fields()
                self.index_instance.update_teachers_count()
                teacher_id = get_teachers_sequence()
                for subject in selected_subjects:
                    add_teacher_subject(teacher_id,subject)
                self.clear_checkbox_selection()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return


        evaluate = add_teacher(full_name, phone, email,gender,address)
        if evaluate == "Teacher added successfully":
            selected_subjects = self.get_selected_subjects()
            QMessageBox.information(self, "info", f"{evaluate}")
            self.clear_fields()
            self.index_instance.update_teachers_count()
            teacher_id = get_teachers_sequence()
            for subject in selected_subjects:
                add_teacher_subject(teacher_id,subject)
            self.clear_checkbox_selection()
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")


        

