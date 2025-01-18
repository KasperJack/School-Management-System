
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QToolButton
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

import School_System.helpers.db_utils as database
from School_System.ui import VIEW_CLASS_DIALOG


class ViewClassDialog(QDialog):
    def __init__(self, index_instance, class_id=None, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance  #main class instance
        self.class_id = class_id
        uic.loadUi(VIEW_CLASS_DIALOG, self)

        self.setWindowTitle("View Class")

        #print(f"Class ID: {self.class_id}")

        class_data, teachers_data, students_data = database.get_class_info_edit(self.class_id)


        #print(class_data)  = (27, 'class 44', 'CAP', 'october', 70, '2025-01-18', 2)

        #print(teachers_data) = [('Aron Smith', 'math'), ('John Doe', 'science')]
        #print(students_data)

        print(students_data)
        self.class_name.setText(class_data[1])
        self.grade.setText(class_data[2])
        self.sesstion.setText(class_data[3])
        self.creation_date.setText(class_data[5])
        self.max_stud.setText(f"{class_data[6]}/{class_data[4]}")





        # Set row and column counts
        self.teachers_table.setRowCount(len(teachers_data))
        self.teachers_table.setColumnCount(4)  # ts_id, teacher_id, subject_name, full_name

        # Populate the table
        for row_index, row_data in enumerate(teachers_data):
            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.teachers_table.setItem(row_index, col_index, item)

        # Set the header labels
        self.teachers_table.setHorizontalHeaderLabels(["TS ID", "Teacher ID", "Subject", "Teacher Name"])
        self.teachers_table.setColumnHidden(0, True)
        self.teachers_table.setColumnHidden(1, True)

        students_data = [
            (225, None, "Jacob Seed"),
            (226, None, "Hope Smith")
        ]




        # Set up a container widget for the scroll area
        container_widget = QWidget()
        layout = QVBoxLayout(container_widget)

        # Create student cards and add to the layout
        for student_id, photo_data, full_name in students_data:
            student_card = StudentCard(student_id, photo_data, full_name)
            student_card.button_clicked.connect(
                self.on_student_card_button_click)  # Connect to the button click handler
            layout.addWidget(student_card)

        # Add stretch at the end of the layout
        layout.addStretch()

        # Set the container widget as the scroll area's widget
        self.scrollArea_students.setWidget(container_widget)
        self.scrollArea_students.setWidgetResizable(True)

    def on_student_card_button_click(self, student_id):
        print(f"Button clicked for student ID: {student_id}")
        # Now you can handle the student_id in the main class or perform other actions















class StudentCard(QWidget):
    # Signal to emit when the button is clicked, passing the student_id
    button_clicked = pyqtSignal(int)

    def __init__(self, student_id, photo_data, full_name, parent=None):
        super().__init__(parent)

        self.student_id = student_id  # Store the student_id

        # Split full_name into first name and last name
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Layouts
        main_layout = QHBoxLayout()
        info_layout = QVBoxLayout()

        # Photo Label
        self.photo_label = QLabel(self)
        self.photo_label.setFixedSize(64, 64)
        if photo_data:
            pixmap = QPixmap()
            pixmap.loadFromData(photo_data)
            self.photo_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.photo_label.setText("No Photo")  # Placeholder if no photo

        # Name Labels
        self.first_name_label = QLabel(first_name, self)
        self.last_name_label = QLabel(last_name, self)

        # Add to info layout
        info_layout.addWidget(self.first_name_label)
        info_layout.addWidget(self.last_name_label)

        # Tool Button
        self.tool_button = QToolButton(self)
        self.tool_button.setText("...")
        self.tool_button.setFixedSize(24, 24)
        self.tool_button.clicked.connect(self.on_button_clicked)  # Connect button click

        # Combine layouts
        main_layout.addWidget(self.photo_label)
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.tool_button)
        self.setLayout(main_layout)

    def on_button_clicked(self):
        """Emit signal with student_id when the button is clicked."""
        self.button_clicked.emit(self.student_id)