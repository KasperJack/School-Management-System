
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView, QTableWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt

import School_System.helpers.db_utils as database
from School_System.ui import EDIT_CLASS_DIALOG
from School_System.resources import  ICONS


class EditClassDialog(QDialog):
    def __init__(self, index_instance, class_id=None, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance  #main class instance
        self.class_id = class_id
        uic.loadUi(EDIT_CLASS_DIALOG, self)

        self.setWindowTitle("Edit Class")

        print(f"Class ID: {self.class_id}")

        #class_data, teachers_data, students_data = database.get_class_info_edit(self.class_id)


        #print(class_data)  = (27, 'class 44', 'CAP', 'october', 70, '2025-01-18', 2)

        #print(teachers_data) = [('Aron Smith', 'math'), ('John Doe', 'science')]
        #print(students_data)


        #get_students_no_class
        #get_students_in_class





        # Set the header labels
        #self.students_in_class.setColumnHidden(0, True)
        #self.students_in_class.setColumnHidden(1, True)

        self.setup_class_transfer_tables()

        self.add_std_button.setEnabled(False)
        self.remove_std_button.setEnabled(False)


        self.no_class_table.cellClicked.connect(self.on_cell_clicked_no_class)
        self.this_class_table.cellClicked.connect(self.on_cell_clicked_class)


        self.add_std_button.clicked.connect(self.add_student_to_class)
        self.remove_std_button.clicked.connect(self.remove_student_from_class)







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
        print(id)


    def remove_student_from_class(self):
        selected_row = self.this_class_table.currentRow()

        item = self.this_class_table.item(selected_row, 0)
        id = item.text()
        print(id)



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

