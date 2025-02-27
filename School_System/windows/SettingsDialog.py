from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import SETTINGS_DIALOG





class SettingsDialog(QDialog):
    def __init__(self, index_instance ,user_id= None ,parent=None):
        super().__init__(parent)
        uic.loadUi(SETTINGS_DIALOG, self)
        self.index_instance = index_instance  # main class instance
        self.user_id = user_id
        self.setWindowTitle("settings")
        print(self.user_id)

