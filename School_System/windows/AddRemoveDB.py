
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QRadioButton, QPushButton, QDialog, QMessageBox,QAbstractItemView,QHeaderView
from PyQt6 import uic
from PyQt6.QtCore import Qt


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

        self.add_db_button.clicked.connect(self.add_data_base)
        self.close_button.clicked.connect(self.close)

        self.set_up_db_selction_table()




    def set_up_db_selction_table(self):
        self.db_table.setColumnCount(3)  # Three columns (Radio, Database Name, Delete Button)
        self.db_table.setHorizontalHeaderLabels(["Select", "Database Name", "Delete"])
        self.db_table.verticalHeader().setVisible(False)

        self.db_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.db_table.setShowGrid(False)

        # self.classes_table.setSelectionBehavior(self.classes_table.SelectionBehavior.SelectRows)
        self.db_table.setSelectionMode(self.db_table.SelectionMode.NoSelection)
        self.db_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        header = self.db_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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
            database.update_route()



    def delete_database(self, db_name):

        confirmation = QMessageBox.question(
            self,
            "TRASH ?",
            f"Are you sure you want to delete the db",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_database(db_name)
            self.populate_table()











    def add_data_base(self):

        db_name = self.db_name.text()

        if not db_name:
            return

        for row in range(self.db_table.rowCount()):
            existing_db_name = self.db_table.item(row, 1).text()
            if existing_db_name == db_name:
                print("Database name already exists!")
                return

        self.db_manager.create_new_db(db_name)
        self.populate_table()
