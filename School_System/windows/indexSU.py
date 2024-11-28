import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic



class indexSU(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'indexSU.ui')
        uic.loadUi(ui_path, self)

    
    