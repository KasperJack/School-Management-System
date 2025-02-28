from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
import School_System.helpers.db_utils as database
import School_System.helpers.strings as fmt
from School_System.ui import ADD_REMOVE_DB

from PyQt6.QtCore import  Qt






class AddRemoveDB(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ADD_REMOVE_DB, self)

        self.setWindowTitle("Add Database")

        self.create_account_button.clicked.connect(self.create_account)









