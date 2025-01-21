from time import sleep

from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView, QTableWidget, QComboBox
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QIcon
from PyQt6.QtCore import Qt

import School_System.helpers.db_utils as database
from School_System.helpers.db_utils import add_subject_to_default_teacher
from School_System.ui import EDIT_CLASS_DIALOG
from School_System.resources import  ICONS


class EditClassDialog(QDialog):
    def __init__(self, index_instance, class_id=None, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance  #main class instance
        self.class_id = class_id
        uic.loadUi(EDIT_CLASS_DIALOG, self)

        self.setWindowTitle("Edit Class")


        self.setup_class_transfer_tables()




        self.no_class_table.cellClicked.connect(self.on_cell_clicked_no_class)
        self.this_class_table.cellClicked.connect(self.on_cell_clicked_class)

        self.add_std_button.clicked.connect(self.add_student_to_class)
        self.remove_std_button.clicked.connect(self.remove_student_from_class)




        #class_data, teachers_data, students_data = database.get_class_info_edit(self.class_id)
        #print(teachers_data)
        self.reload()
        self.new_subjects_table.setColumnHidden(0, True)





    def on_cell_clicked_no_class(self, row, column):
        # Deselect all selected cells in the table
        self.this_class_table.clearSelection()

        self.remove_std_button.setEnabled(False)
        #light the add  button
        self.add_std_button.setEnabled(True)  # Re-enables the button


    def add_student_to_class(self):
        selected_row = self.no_class_table.currentRow()

        item = self.no_class_table.item(selected_row, 0)
        id = item.text()
        database.assign_student_to_class(id, self.class_id)
        self.load_students_no_class()
        self.load_students_in_class()



    def remove_student_from_class(self):
        selected_row = self.this_class_table.currentRow()

        item = self.this_class_table.item(selected_row, 0)
        id = item.text()
        database.remove_student_from_class(id)
        self.load_students_no_class()
        self.load_students_in_class()




    def on_cell_clicked_class(self, row, column):
        self.no_class_table.clearSelection()
        #remove selection frol the other tabe
        self.add_std_button.setEnabled(False)
        #light the add  button
        self.remove_std_button.setEnabled(True)  # Re-enables the button












    def load_students_no_class(self):
        students_no_class = database.get_students_no_class()
        self.no_class_table.setRowCount(len(students_no_class))
        self.no_class_table.setColumnCount(3)
        self.no_class_table.setHorizontalHeaderLabels(["ID", "Full Name", "Birth Date"])

        # Populate the table
        for row_index, row_data in enumerate(students_no_class):
            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.no_class_table.setItem(row_index, col_index, item)




    def load_students_in_class(self):

        students_in_class = database.get_students_in_class(self.class_id)

        self.this_class_table.setRowCount(len(students_in_class))
        self.this_class_table.setColumnCount(3)
        self.this_class_table.setHorizontalHeaderLabels(["ID", "Full Name", "Birth Date"])

        # Populate the table
        for row_index, row_data in enumerate(students_in_class):
            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.this_class_table.setItem(row_index, col_index, item)




    def setup_class_transfer_tables(self):
        self.add_std_button.setEnabled(False)
        self.remove_std_button.setEnabled(False)
        self.no_class_table.verticalHeader().setVisible(False)
        #self.no_class_table.horizontalHeader().hide()

        self.no_class_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.no_class_table.setShowGrid(False)
        # Set selection behavior to select rows
        self.no_class_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.no_class_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) ## only one selection

        self.load_students_no_class()
        self.no_class_table.setColumnHidden(0, True)




        self.this_class_table.verticalHeader().setVisible(False)
        #self.no_class_table.horizontalHeader().hide()

        self.this_class_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.this_class_table.setShowGrid(False)
        # Set selection behavior to select rows
        self.this_class_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.this_class_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) ## only one selection
        self.load_students_in_class()
        self.this_class_table.setColumnHidden(0, True)



        self.subjects_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.subjects_table.setShowGrid(False)
        self.subjects_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.subjects_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.subjects_table.verticalHeader().setVisible(False)




#######################################################################################################################

    def load_subjects_with_teachers(self, subjects_data, teacher_assignments):
        # teacher_assignments: List of tuples (subject_id, teacher_id)

        # Update the column count to include two extra columns (empty before and after "Teacher")
        self.subjects_table.setRowCount(len(subjects_data))
        self.subjects_table.setColumnCount(6)
        self.subjects_table.setHorizontalHeaderLabels(["#", "Subject Name", "Before", "Teacher", "After", "Actions"])

        # Populate the table
        for row_index, subject in enumerate(subjects_data):
            # Add Subject ID
            subject_id_item = QTableWidgetItem(str(subject['subject_id']))
            subject_id_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.subjects_table.setItem(row_index, 0, subject_id_item)

            # Add Subject Name
            subject_name_item = QTableWidgetItem(subject['subject_name'])
            subject_name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.subjects_table.setItem(row_index, 1, subject_name_item)

            # Add empty "Before" column with an icon
            before_item = QTableWidgetItem()
            before_item.setIcon(QIcon(f"{ICONS}/user.png"))  # Replace with the actual path to your icon
            before_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Non-editable cell
            self.subjects_table.setItem(row_index, 2, before_item)

            # Add a combo box for Teachers
            teachers_combo = QComboBox()
            for teacher_id, teacher_name in subject['teachers']:
                teachers_combo.addItem(teacher_name, userData=teacher_id)  # Store teacher ID as userData

            # Check if this subject has an assigned teacher
            assigned_teacher_id = next(
                (teacher_id for subj_id, teacher_id in teacher_assignments if subj_id == subject['subject_id']),
                None
            )
            if assigned_teacher_id is not None:
                # Set the combo box to the assigned teacher
                for i in range(teachers_combo.count()):
                    if teachers_combo.itemData(i) == assigned_teacher_id:
                        teachers_combo.setCurrentIndex(i)
                        break

            # Connect signal for teacher selection
            teachers_combo.currentIndexChanged.connect(self.teacher_selection_changed)
            self.subjects_table.setCellWidget(row_index, 3, teachers_combo)

            # Add empty "After" column
            after_item = QTableWidgetItem("")
            after_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.subjects_table.setItem(row_index, 4, after_item)

            # Add a "Remove" button
            remove_button = QPushButton("Remove")
            remove_button.setStyleSheet("color: red; font-weight: bold;")  # Optional: Style the button
            remove_button.clicked.connect(lambda _, row=row_index: self.remove_teacher(row))

            # Add the button to the table
            self.subjects_table.setCellWidget(row_index, 5, remove_button)



    def teacher_selection_changed(self):
        # Get the sender (the combo box that triggered the signal)
        combo_box = self.sender()
        if combo_box:
            # Find the row where the combo box is located
            row = self.subjects_table.indexAt(combo_box.pos()).row()

            # Get Subject ID from the first column of the row
            subject_id_item = self.subjects_table.item(row, 0)
            subject_id = int(subject_id_item.text()) if subject_id_item else None

            # Get selected Teacher Name and ID
            teacher_name = combo_box.currentText()
            teacher_id = combo_box.currentData()  # Retrieve hidden userData (teacher ID)

            print(f"Subject ID: {subject_id}, Selected Teacher ID: {teacher_id}, Teacher Name: {teacher_name}")
            database.change_course_teacher(teacher_id,subject_id,self.class_id)



    def remove_teacher(self, row_index):
        # Get Subject ID from the first column
        subject_id_item = self.subjects_table.item(row_index, 0)  # Column 0 for Subject ID
        subject_id = int(subject_id_item.text()) if subject_id_item else None

        # Get the teacher combo box from the "Teacher" column (column 3)
        combo_box = self.subjects_table.cellWidget(row_index, 3)  # Column 3 for Teacher
        if combo_box and isinstance(combo_box, QComboBox):
            teacher_id = combo_box.currentData()  # Retrieve hidden userData (teacher ID)
            teacher_name = combo_box.currentText()

            print(f"Remove Teacher: {teacher_name} (ID: {teacher_id}) from Subject ID: {subject_id}")

            # Call the database function to remove the teacher assignment
            database.remove_class_course(teacher_id, subject_id)

            # Reload the table to reflect changes
            self.reload()



    def load_subjects_with_add_button(self, subjects_data, excluded_subjects):
        # Extract the subject IDs from the excluded_subjects list
        excluded_ids = {subject_id for subject_id, _ in excluded_subjects}

        # Filter out subjects that are in the excluded list
        filtered_subjects = [subject for subject in subjects_data if subject[0] not in excluded_ids]

        # Set up the table
        self.new_subjects_table.setRowCount(len(filtered_subjects))
        self.new_subjects_table.setColumnCount(3)
        self.new_subjects_table.setHorizontalHeaderLabels(["Subject ID", "Subject Name", "Actions"])

        # Populate the table with filtered subjects
        for row_index, (subject_id, subject_name) in enumerate(filtered_subjects):
            # Add Subject ID
            subject_id_item = QTableWidgetItem(str(subject_id))
            subject_id_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.new_subjects_table.setItem(row_index, 0, subject_id_item)

            # Add Subject Name
            subject_name_item = QTableWidgetItem(subject_name)
            subject_name_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.new_subjects_table.setItem(row_index, 1, subject_name_item)

            # Add an "Add" button
            add_button = QPushButton("Add")
            add_button.setStyleSheet("color: green; font-weight: bold;")  # Optional: Style the button
            add_button.clicked.connect(lambda _, row=row_index: self.add_subject(row))  # Connect to a custom method
            self.new_subjects_table.setCellWidget(row_index, 2, add_button)

    def add_subject(self, row):
        subject_id = self.new_subjects_table.item(row, 0).text()
        database.add_subject_to_class(subject_id, self.class_id)
        self.reload()



    def reload(self):
        data = database.get_class_subjects_and_all_teachers(self.class_id)
        ids = database.get_class_subjects_and_teachers(self.class_id)

        self.load_subjects_with_teachers(data,ids)

        subjects = database.get_subjects()
        self.load_subjects_with_add_button(subjects,ids)
