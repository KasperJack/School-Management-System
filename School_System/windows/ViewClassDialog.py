
from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6 import uic
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

        class_data, teachers_data, students_data = database.get_class_info(self.class_id)


        #print(class_data)  = (27, 'class test88', 'CAP', 'october', 70, '2025-01-18', 2)

        #print(teachers_data) = [('Aron Smith', 'math'), ('John Doe', 'science')]
        #print(students_data)

        print(class_data)
        self.class_name.setText(class_data[1])
        self.grade.setText(class_data[2])
        self.sesstion.setText(class_data[3])
        self.creation_date.setText(class_data[5])
        self.max_stud.setText(f"{class_data[6]}/{class_data[4]}")


        # Assuming teachers_table is your QTableWidget
        self.teachers_table.setRowCount(len(teachers_data))  # Set the number of rows
        self.teachers_table.setColumnCount(2)  # Set the number of columns

        # Set header labels (if required)
        self.teachers_table.setHorizontalHeaderLabels(['Subject', 'Teacher'])

        # Add data to the table
        for row_index, row_data in enumerate(teachers_data):
            # Rearrange data: ('Subject', 'Name') instead of ('Name', 'Subject')
            subject, name = row_data[1], row_data[0]

            # Insert into table
            self.teachers_table.setItem(row_index, 0, QTableWidgetItem(subject))  # Subject in column 0
            self.teachers_table.setItem(row_index, 1, QTableWidgetItem(name))  # Name in column 1
