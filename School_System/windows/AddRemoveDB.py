
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QRadioButton, QPushButton, QDialog, QMessageBox
import os
from PyQt6 import uic

import School_System.helpers.db_utils as database
import School_System.helpers.strings as fmt
from School_System.ui import ADD_REMOVE_DB


from School_System.db.DatabaseManager import db_manager_instance





class AddRemoveDB(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ADD_REMOVE_DB, self)
        self.db_manager = db_manager_instance
        self.setWindowTitle("Add Database")

        self.set_up_db_selction_table()




    def set_up_db_selction_table(self):
        self.db_table.setColumnCount(3)  # Three columns (Radio, Database Name, Delete Button)
        self.db_table.setHorizontalHeaderLabels(["Select", "Database Name", "Delete"])
        self.populate_table()



    def populate_table(self):
        """Populate the table with databases from the manager."""
        db_files = self.db_manager.get_all_databases()

        # Set row count to match the number of databases
        self.db_table.setRowCount(len(db_files))

        for row, db_file in enumerate(db_files):
            # Extract the database name (remove the extension and "(current)" indicator)
            db_name = db_file.replace(" (current)", "").replace(".db", "")
            # Create a radio button
            radio_button = QRadioButton()
            radio_button.setChecked(db_file.endswith("(current)"))
            radio_button.toggled.connect(
                lambda checked, db_name=db_file.replace(" (current)", ""): self.on_radio_button_toggled(checked, db_name))
            self.db_table.setCellWidget(row, 0, radio_button)  # Place radio button in the first column

            # Set the database name in the second column
            self.db_table.setItem(row, 1, QTableWidgetItem(db_name))

            # Create a delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, db_name=db_file.replace(" (current)", ""): self.delete_database(db_name))
            self.db_table.setCellWidget(row, 2, delete_button)  # Place delete button in the third column


    def on_radio_button_toggled(self, checked, db_name):
        """Handle the radio button toggle event."""
        if checked:

            #print(f"Selected Database: {db_name}")
            #self.db_manager.change_database(db_name)
            self.db_manager.change_database(db_name)



    def delete_database(self, db_name):
        print(db_name)




    def add_data_base(self):
        pass