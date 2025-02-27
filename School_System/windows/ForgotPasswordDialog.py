from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import FORGET_PASSWORD_DIALOG
import bcrypt
from PyQt6.QtCore import  Qt






class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(FORGET_PASSWORD_DIALOG, self)

        self.setWindowTitle("forget password")

        self.check_mail_button.clicked.connect(self.check_email)







    def check_email(self):
        pass








