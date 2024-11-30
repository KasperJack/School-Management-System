import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem
from PyQt6 import uic

import sqlite3
from School_System.db.dbio import connect




class indexSU(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'indexSU.ui')
        uic.loadUi(ui_path, self)

        self.tableWidget.verticalHeader().setVisible(False)

        
        self.subject_button.clicked.connect(self.hide_data)
        self.load_inactive_users()











    def hide_data(self):
        self.tableWidget.hide()

    

    def add_entry_to_table(self):
        # Define the data
        id_ = "1"
        name = "John Doe"
        email = "john.doe@example.com"
        
        # Get the table widget from the UI
        table = self.tableWidget
        
        # Insert a new row
        row_position = table.rowCount()
        table.insertRow(row_position)  # Adds a new row at the end
        
        # Populate the row with data
        table.setItem(row_position, 0, QTableWidgetItem(id_))    # First column
        table.setItem(row_position, 1, QTableWidgetItem(name))  # Second column
        table.setItem(row_position, 2, QTableWidgetItem(email)) # Third column





    def load_inactive_users(self):
        # Connect to the database
        db_path = connect()  # Replace with your database connection method
        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()

            # Query to fetch inactive users
            query = """
                SELECT full_name, email, registration_date 
                FROM users 
                WHERE status = 'inactive'
            """
            cursor.execute(query)
            results = cursor.fetchall()

            # Set up the table widget for 3 columns
            self.tableWidget.setRowCount(len(results))  # Set rows based on query result count
            self.tableWidget.setColumnCount(3)  # Set columns for "Full Name", "Email", "Registration Date"
            self.tableWidget.setHorizontalHeaderLabels(["Full Name", "Email", "Registration Date"])

            # Populate the table
            for row_index, row_data in enumerate(results):
                for col_index, data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            # Adjust columns to fit contents
            self.tableWidget.resizeColumnsToContents()


    