from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QDate,QDateTime

import School_System.helpers.db_utils as database

from School_System.ui import ADD_EVENT_DIALOG





class AddEventDialog(QDialog):
    def __init__(self, index_instance ,user_id= None ,parent=None):
        super().__init__(parent)
        uic.loadUi(ADD_EVENT_DIALOG, self)
        self.index_instance = index_instance  # main class instance
        self.user_id = user_id
        self.setWindowTitle("add event")
        #print(self.user_id)
        self.add_event_button.clicked.connect(self.add_event)
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())



    def add_event(self):
        event_name = self.event_name.text()
        date = self.datetime_edit.date()

        if not event_name: return


        database.add_event(date,Event(event_name, QColor(255, 22, 0, 180)))
        self.index_instance.load_events()
        self.event_name.clear()







class Event:
    def __init__(self, title, color=QColor(255, 100, 100, 180)):
        self.title = title
        self.color = color