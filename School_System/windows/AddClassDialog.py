import os

from PyQt6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QCheckBox
from PyQt6 import uic
from School_System.helpers.db_utils import *



class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddClassDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Class")

        self.add_class_button.clicked.connect(self.add_class)
        grades = get_grades()
        self.grades_dropdown.addItems(grades)
        self.load_teachers_subjects()




    



    def load_teachers_subjects(self):
        """Fetch teacher-subject pairs from the database and populate the teachers_subjects_scrollArea with checkboxes."""
        db_path = connect()
        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()
            # Query to fetch teacher-subject pairs
            cursor.execute("""
                SELECT ts.id, sub.subject_name, t.full_name
                FROM teachers_subjects ts
                JOIN subjects sub ON ts.subject_id = sub.subject_id
                JOIN teachers t ON ts.teacher_id = t.teacher_id
            """)
            teachers_subjects = cursor.fetchall()

        # Access or create the scroll area widget
        scroll_widget = self.teachers_subjects_scrollArea.widget()
        if scroll_widget is None:
            scroll_widget = QWidget()
            self.teachers_subjects_scrollArea.setWidget(scroll_widget)
            self.teachers_subjects_scrollArea.setWidgetResizable(True)

        # Set up a layout if not already present
        if scroll_widget.layout() is None:
            scroll_widget.setLayout(QVBoxLayout())

        layout = scroll_widget.layout()

        # Clear existing widgets in the layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add checkboxes for each teacher-subject pair
        for pair_id, subject_name, teacher_name in teachers_subjects:
            display_text = f"{subject_name} ({teacher_name})"  # Format the display
            checkbox = QCheckBox(display_text, self)
            checkbox.setObjectName(f"checkbox_{pair_id}")  # Use pair ID in the object name
            checkbox.setProperty("pair_id", pair_id)  # Store the pair ID as a property
            layout.addWidget(checkbox)

    def get_selected_teachers_subjects(self):
        """Retrieve IDs of selected teacher-subject pairs from the scroll area."""
        selected_pair_ids = []

        # Access the widget inside the scroll area
        scroll_widget = self.teachers_subjects_scrollArea.widget()
        if scroll_widget is None or scroll_widget.layout() is None:
            print("Error: Scroll area does not have a proper widget or layout.")
            return selected_pair_ids  # Return an empty list if layout is missing

        layout = scroll_widget.layout()

        # Iterate through the items in the layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()

            # Check if the widget is a QCheckBox and is checked
            if isinstance(widget, QCheckBox) and widget.isChecked():
                # Retrieve the pair ID stored in the checkbox property
                pair_id = widget.property("pair_id")
                if pair_id is not None:
                    selected_pair_ids.append(pair_id)

        return selected_pair_ids



    def clear_checkbox_selection(self):
        """Clear all checkbox selections in the teachers_subjects_scrollArea."""
        # Access the widget inside the scroll area
        scroll_widget = self.teachers_subjects_scrollArea.widget()

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










    def add_class(self):

        #info from input fields
        class_name = self.class_name_field.text()
        grade_name = self.grades_dropdown.currentText()

        # Validate input fields
        if not class_name or not grade_name:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return


        evaluate = add_class(class_name,grade_name)
        get_selected_teachers_subjects = self.get_selected_teachers_subjects()
        if evaluate == "Class added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.class_name_field.clear()
            for teacher_subject in get_selected_teachers_subjects:
                add_course(teacher_subject,class_name)
                self.clear_checkbox_selection()
            return
        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")






        

