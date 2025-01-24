
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView,QTreeWidget, QTreeWidgetItem,QMenu
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor ,QBrush


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



        self.tree_widget.setHeaderLabel("Subjects and Classes")  # Se
        self.tree_widget.setColumnCount(2)

        self.add_subjects()
        self.add_classes_and_grades()



        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)



    def add_subjects(self):
        all_subjects = database.get_teacher_subjects(self.teacher_id)
        for subject_id, subject_name in all_subjects:
            subject_item = QTreeWidgetItem(self.tree_widget)
            subject_item.setText(0, subject_name)  # Set the subject name

            # Store the subject ID in the item
            subject_item.setData(0, Qt.ItemDataRole.UserRole, subject_id)




    def add_classes_and_grades(self):
        test = database.get_teacher_classes(self.teacher_id)

        for subject_id, class_name, class_id, grade, ts_id in test:
            # Find the subject item by its ID
            subject_item = self.find_subject_item(subject_id)
            if subject_item:
                # Add the class and grade as a child item under the subject
                class_item = QTreeWidgetItem(subject_item)
                class_item.setText(0, class_name)  # Set the class name in the second column
                class_item.setText(1, grade)  # Set the grade in the third column

                # Store the class_id and ts_id in the item
                class_item.setData(0, Qt.ItemDataRole.UserRole, class_id)  # Store class_id
                class_item.setData(1, Qt.ItemDataRole.UserRole, ts_id)  # Store ts_id


    def find_subject_item(self, subject_id):
        # Find the subject item by its ID
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.data(0, Qt.ItemDataRole.UserRole) == subject_id:
                return item
        return None



    def show_context_menu(self, position: QPoint):
        # Get the item at the clicked position
        item = self.tree_widget.itemAt(position)

        if item:  # Only show the context menu if an item exists at the position
            # Create the context menu
            context_menu = QMenu(self)

            # Add actions to the menu
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")

            # Show the menu at the global position
            action = context_menu.exec(self.tree_widget.viewport().mapToGlobal(position))

            # Handle actions
            if action == edit_action:
                print("Edit action triggered")
                # Implement edit functionality
            elif action == delete_action:
                print("Delete action triggered")
                # Implement delete functionality
