
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView,QTreeWidget, QTreeWidgetItem
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt

import School_System.helpers.db_utils as database
from School_System.ui import EDIT_TEACHER_DIALOG
from School_System.resources import  ICONS


class EditTeacherDialog(QDialog):



    def __init__(self, index_instance, teacher_id=None, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance  #main class instance
        self.teacher_id = teacher_id
        uic.loadUi(EDIT_TEACHER_DIALOG, self)

        self.setWindowTitle("Edit Teacher")

        test = database.get_teacher_classes(self.teacher_id)
        print(test)
        all_subjects = database.get_teacher_subjects(self.teacher_id)
        print(all_subjects)

        self.tree_widget.setHeaderLabel("Subjects and Classes")  # Se
        self.tree_widget.setColumnCount(3)

        self.add_subjects()# t the header

    def add_subjects(self):
        all_subjects = database.get_teacher_subjects(self.teacher_id)
        for subject_id, subject_name in all_subjects:
            subject_item = QTreeWidgetItem(self.tree_widget)
            subject_item.setText(0, subject_name)  # Set the subject name

            # Store the subject ID in the item
            subject_item.setData(0, Qt.ItemDataRole.UserRole, subject_id)