
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView
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

        print(f"t ID: {self.teacher_id}")



