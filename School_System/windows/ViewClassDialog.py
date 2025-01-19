
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView
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

        self.setup_students_table(students_data)


        #print(students_data)
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








    def setup_students_table(self, students_data):
        self.students_table.verticalHeader().setVisible(False)

        self.students_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.students_table.setShowGrid(False)

        #self.classes_table.setSelectionBehavior(self.classes_table.SelectionBehavior.SelectRows)
        self.students_table.setSelectionMode(self.students_table.SelectionMode.NoSelection)
        self.students_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.load_students(students_data)
        self.students_table.setWordWrap(True)

        header = self.students_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set specific columns to have a fixed size
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        #header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

        # Set the fixed size for these columns
        header.resizeSection(1, 70)
        header.resizeSection(2, 100)
        header.resizeSection(3, 50)
        #header.resizeSection(6, 190)














    def load_students(self, students_data):
        self.students_table.setRowCount(len(students_data))
        self.students_table.setColumnCount(4)  # Add an extra column for actions
        self.students_table.setHorizontalHeaderLabels(["ID", "Photo", "Name", "Actions"])
        self.students_table.setColumnHidden(0, True)  # Hide the "ID" column

        # Populate the table
        for row_index, (student_id, photo, name) in enumerate(students_data):
            namer = name.replace(" ", "\n")  # Replace spaces with line breaks
            id_item = QTableWidgetItem(str(student_id))
            self.students_table.setItem(row_index, 0, id_item)

            # Photo Column
            if photo is not None:
                pixmap = QPixmap()
                pixmap.loadFromData(photo)  # Assuming `photo` is binary image data
                label = QLabel()
                label.setPixmap(pixmap.scaled(50, 50))  # Resize the image to 50x50
                self.students_table.setCellWidget(row_index, 1, label)
            else:
                placeholder = QLabel("No Photo")
                self.students_table.setCellWidget(row_index, 1, placeholder)

            # Name Column
            name_item = QTableWidgetItem(namer)
            self.students_table.setItem(row_index, 2, name_item)

            # Actions Column
            view_button = QPushButton("?")
            view_button.setStyleSheet("background-color: blue; color: white;")

            # Connect buttons to their respective methods
            view_button.clicked.connect(lambda _, sid=student_id: self.view_student(sid))

            # Add buttons to a layout
            button_layout = QHBoxLayout()
            button_layout.addWidget(view_button)

            # Create a widget to hold the buttons
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # Add the widget to the table
            self.students_table.setCellWidget(row_index, 3, button_widget)  # Column 3 is the "Actions" column
            for row in range(self.students_table.rowCount()):
                self.students_table.setRowHeight(row, 55)









        # Create a table widget





    def view_student(self, student_id):
        """Handle the 'View' button click."""
        print(f"View Student ID: {student_id}")










