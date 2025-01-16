


from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import ADD_SUBJECT_DIALOG


class AddSubjectDialog(QDialog):
    def __init__(self,index_instance ,parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(ADD_SUBJECT_DIALOG, self)

        self.setWindowTitle("Add Subject")

        self.add_subject_button.clicked.connect(self.add_subject)





    
    
    
    
    def add_subject(self):


        # Get info from input fields
        subject_name = self.subject_name_field.text()
        description = self.description_field.text()

        # Validate input fields
        if not subject_name:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        if not description:
            evaluate = database.add_subject(subject_name)
            if evaluate == "Subject added successfully":
                QMessageBox.information(self, "info", f"{evaluate}")
                self.subject_name_field.clear()
                self.index_instance.refresh_setup_activity_log__table()
                return
            else:
                QMessageBox.warning(self, "Error", f"{evaluate}")
                return



        evaluate = database.add_subject(subject_name,description)

        if evaluate == "Subject added successfully":
            QMessageBox.information(self, "info", f"{evaluate}")
            self.subject_name_field.clear()
            self.description_field.clear()
            self.index_instance.refresh_setup_activity_log__table()
            return

        else:
            QMessageBox.warning(self, "Error", f"{evaluate}")




        

