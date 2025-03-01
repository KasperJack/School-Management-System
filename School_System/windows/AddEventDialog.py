from PyQt6 import uic
from PyQt6.QtGui import QTextDocument, QPainter
from PyQt6.QtPrintSupport import QPrinter
from fontTools.tfmLib import PASSTHROUGH
from fontTools.varLib.models import nonNone
from PyQt6.QtCore import pyqtSlot

import School_System.helpers.db_utils as database

from School_System.ui import ADD_EVENT_DIALOG


class AddEventDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(ADD_EVENT_DIALOG, self)

        self.setWindowTitle("Export pdf")
        self.classes = database.get_classes_ids_grades()


        ##self.index_instance.students_table
        self.close_button.clicked.connect(self.init_export)



