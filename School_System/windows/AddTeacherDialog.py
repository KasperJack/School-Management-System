

from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox, QCheckBox, QHBoxLayout, QLabel, QVBoxLayout ,QGridLayout,QWidget,QGraphicsDropShadowEffect
from PyQt6 import uic
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


import School_System.helpers.db_utils as database
from School_System.ui import ADD_TEACHER_DIALOG # UI FILE


class AddTeacherDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(ADD_TEACHER_DIALOG, self)

        self.setWindowTitle("Add Teacher")

        self.add_teacher_button.clicked.connect(self.add_teacher)
        self.load_subjects()




        self.apply_floating_effect(self.add_teacher_button)
        #self.apply_floating_effect(self.pushButton)
        self.apply_floating_effect(self.email_field)
        self.apply_floating_effect(self.widget)
        self.apply_floating_effect(self.widget_2)
        self.apply_floating_effect(self.serach_subject)





















    def load_subjects(self):

        subjects = database.get_subjects()

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

        self.m_radioButton.setAutoExclusive(False)
        self.f_radioButton.setAutoExclusive(False)


        self.m_radioButton.setChecked(False)
        self.f_radioButton.setChecked(False)

        self.m_radioButton.setAutoExclusive(True)
        self.f_radioButton.setAutoExclusive(True)




    def apply_floating_effect(self, widget):
        # Create a subtle shadow effect
        shadow_effect = QGraphicsDropShadowEffect()

        # Make the shadow effect more subtle
        shadow_effect.setBlurRadius(5)  # Reduced blur radius for a softer shadow
        shadow_effect.setOffset(1, 1)  # Reduced offset for a minimal floating effect
        shadow_effect.setColor(QColor(0, 0, 0, 50))  # Lighter shadow color (lower alpha for subtlety)

        # Apply the effect to the widget
        widget.setGraphicsEffect(shadow_effect)

        # Optional: Slightly raise the widget to enhance the floating effect
        widget.move(widget.x(), widget.y() - 4)  # Raise it just a bit












    def add_teacher(self):
        name =self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        address = self.address_field.text()

        if self.m_radioButton.isChecked():
            gender = "M"
        elif self.f_radioButton.isChecked():
            gender = "F"

        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return






        if not name or not last_name or not email or not phone or not gender:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        if not address:
            evaluate = database.add_teacher(full_name,phone,email,gender)
            selected_subjects = self.get_selected_subjects()
            if evaluate == "Teacher added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.clear_fields()
                self.index_instance.update_teachers_count()
                self.index_instance.refresh_setup_activity_log__table()

                if selected_subjects:
                    teacher_id = database.get_teachers_sequence()
                    for subject in selected_subjects:
                        database.add_teacher_subject(teacher_id, subject)

                self.index_instance.setup_teachers_scroll()
                self.clear_checkbox_selection()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return


        evaluate = database.add_teacher(full_name, phone, email,gender,address)
        if evaluate == "Teacher added successfully":
            selected_subjects = self.get_selected_subjects()
            QMessageBox.information(self, "info", f"{evaluate}")
            self.clear_fields()
            self.index_instance.update_teachers_count()
            self.index_instance.refresh_setup_activity_log__table()

            if selected_subjects:
                teacher_id = database.get_teachers_sequence()
                for subject in selected_subjects:
                    database.add_teacher_subject(teacher_id, subject)

            self.index_instance.setup_teachers_scroll()
            self.clear_checkbox_selection()
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")


        

