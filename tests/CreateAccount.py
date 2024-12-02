from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QTableWidgetItem

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

        # Set up the table widget for 4 columns (adding "Actions")
        self.tableWidget.setRowCount(len(results))  # Set rows based on query result count
        self.tableWidget.setColumnCount(4)  # Adding the "Actions" column
        self.tableWidget.setHorizontalHeaderLabels(["Full Name", "Email", "Registration Date", "Actions"])

        # Populate the table
        for row_index, row_data in enumerate(results):
            for col_index, data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            # Add the "Actions" buttons
            activate_button = QPushButton("Activate")
            delete_button = QPushButton("Delete")

            # Connect buttons to their respective methods
            activate_button.clicked.connect(lambda _, r=row_index: self.activate_user(r))
            delete_button.clicked.connect(lambda _, r=row_index: self.delete_user(r))

            # Add buttons to a layout
            button_layout = QHBoxLayout()
            button_layout.addWidget(activate_button)
            button_layout.addWidget(delete_button)

            # Create a widget to hold the buttons
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # Add the widget to the table
            self.tableWidget.setCellWidget(row_index, 3, button_widget)  # Column 3 is the "Actions" column

        # Adjust columns to fit contents
        self.tableWidget.resizeColumnsToContents()

# Methods to handle the buttons' functionality
def activate_user(self, row_index):
    full_name = self.tableWidget.item(row_index, 0).text()  # Get full_name from row
    email = self.tableWidget.item(row_index, 1).text()  # Get email from row

    # Connect to the database and update the status
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("UPDATE users SET status = 'active' WHERE full_name = ? AND email = ?", (full_name, email))
        db_connection.commit()

    # Optionally refresh the table
    self.load_inactive_users()

def delete_user(self, row_index):
    full_name = self.tableWidget.item(row_index, 0).text()  # Get full_name from row
    email = self.tableWidget.item(row_index, 1).text()  # Get email from row

    # Connect to the database and delete the user
    db_path = connect()
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM users WHERE full_name = ? AND email = ?", (full_name, email))
        db_connection.commit()

    # Optionally refresh the table
    self.load_inactive_users()
