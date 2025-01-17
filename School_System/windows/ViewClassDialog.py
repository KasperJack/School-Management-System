
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import VIEW_CLASS_DIALOG


class ViewClassDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(VIEW_CLASS_DIALOG, self)

        self.setWindowTitle("view Class")





        

