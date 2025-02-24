from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

import School_System.helpers.db_utils as database

from School_System.ui import EXPORT_EXCEL_DIALOG


class ExportExcelDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(EXPORT_EXCEL_DIALOG, self)

        self.setWindowTitle("Export excel")
