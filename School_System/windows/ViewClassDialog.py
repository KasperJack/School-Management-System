
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import VIEW_CLASS_DIALOG


class ViewClassDialog(QDialog):
    def __init__(self, index_instance, class_id=None, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance  # Store the main class instance
        self.class_id = class_id
        uic.loadUi(VIEW_CLASS_DIALOG, self)

        self.setWindowTitle("View Class")

        # Example: Use class_id or index_instance to load data
        print(f"Class ID: {self.class_id}")
        # You can also access `index_instance` to get more data if needed
