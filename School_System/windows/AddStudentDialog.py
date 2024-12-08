import os 
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic




class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'AddStudentDialog.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Add Student")

        self.add_student_button.clicked.connect(self.add_student)




    
    
    def add_student(self):
        pass





        

