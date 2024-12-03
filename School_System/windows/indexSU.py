import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, QScrollArea, QVBoxLayout, QLabel
from PyQt6 import uic
from School_System.windows.AddSubjectDialog import AddSubjectDialog
from School_System.windows.AddTeacherDialog import AddTeacherDialog
import sqlite3
from School_System.db.dbio import connect

import School_System.resources.qrc.rec_rc
from School_System.helpers.db_utils import *




class indexSU(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'indexSU.ui')
        uic.loadUi(ui_path, self)
        self.dashboard_s.clicked.connect(self.sw_dash)
        self.dashboard_b.clicked.connect(self.sw_dash)

        self.subject_s.clicked.connect(self.sw_subject)
        self.subject_b.clicked.connect(self.sw_subject)

        self.classes_s.clicked.connect(self.sw_class)
        self.classes_b.clicked.connect(self.sw_class)

        self.teachers_s.clicked.connect(self.sw_teachers)
        self.teachers_b.clicked.connect(self.sw_teachers)

        self.students_s.clicked.connect(self.sw_students)
        self.students_b.clicked.connect(self.sw_students)
##############################################################
        self.add_subject_button.clicked.connect(self.open_add_subject_dialog)
        self.add_teacher_button.clicked.connect(self.open_add_teacher_dialog)


        self.icon_only.setHidden(True)
        self.tableWidget.verticalHeader().setVisible(False)
        
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)



        # Get the scroll area and its content widget
        self.scrollAreaWidgetContents = self.scrollArea.widget()
        if not self.scrollAreaWidgetContents:
            self.scrollAreaWidgetContents = QWidget()
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Set up a layout for the scroll area's content widget
        self.contentLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.contentLayout)

        # Add some widgets dynamically to test
        for i in range(55):  # Add 5 test labels
            label = QLabel(f"Dynamic Label {i + 1}")
            self.contentLayout.addWidget(label)

        # Add a test button
        button = QPushButton("Dynamic Button")
        button.clicked.connect(lambda: print("Button clicked!"))
        self.contentLayout.addWidget(button)












        
        name = get_logged_in_user()
        self.label_user_name.setText(f"Hello, {name}")
        
        self.load_inactive_users()

        #self.tableWidget.setColumnWidth(0,150)
        #self.tableWidget.setColumnWidth(1,150)
        #self.tableWidget.setColumnWidth(2,150)
        #self.tableWidget.setColumnWidth(3,150)
        # Set the height of all rows to 50 pixels

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, 40)


    def open_add_subject_dialog(self):
        # Create an instance of the AddSubjectDialog
        add_subject_dialog = AddSubjectDialog(self)
        add_subject_dialog.exec()

    def open_add_teacher_dialog(self):
        # Create an instance of the AddTeacherDialog
        add_teacher_dialog = AddTeacherDialog(self)
        add_teacher_dialog.exec()




    def load_inactive_users(self):
            
            results = get_inactive_users()

            # Set up the table widget for 3 columns
            self.tableWidget.setRowCount(len(results))  # Set rows based on query result count
            self.tableWidget.setColumnCount(4)  # Set columns for "Full Name", "Email", "Registration Date"
            self.tableWidget.setHorizontalHeaderLabels(["Full Name", "Email", "Registration Date", "Actions"])

            # Populate the table
            for row_index, row_data in enumerate(results):
                for col_index, data in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))


                # Add the "Actions" buttons
                activate_button = QPushButton("Activate")
                delete_button = QPushButton("Delete")
                activate_button.setStyleSheet("background-color: green; color: white;")
                delete_button.setStyleSheet("background-color: red; color: white;")

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

            #self.tableWidget.resizeColumnsToContents()










    # Methods to handle the buttons' functionality
    def activate_user(self, row_index):
        full_name = self.tableWidget.item(row_index, 0).text()  # Get full_name from row
        email = self.tableWidget.item(row_index, 1).text()  # Get email from row


        # Show a confirmation dialog
        confirmation = QMessageBox.question(
        self,
        "Confirm Activation",
        f"Are you sure you want to activate the user:\n\nName: {full_name}\nEmail: {email}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )


        if confirmation == QMessageBox.StandardButton.Yes:

            activate_admin(full_name,email)
            self.load_inactive_users()

    
    
    def delete_user(self, row_index):
        full_name = self.tableWidget.item(row_index, 0).text()  # Get full_name from row
        email = self.tableWidget.item(row_index, 1).text()  # Get email from row


        # Show a confirmation dialog
        confirmation = QMessageBox.question(
        self,
        "Confirm Deletion",
        f"Are you sure you want to delete the user:\n\nName: {full_name}\nEmail: {email}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )   
       
        if confirmation == QMessageBox.StandardButton.Yes:

            delete_admin(full_name,email)
            self.load_inactive_users()
        










































        #####################################[switching]#############################################
        










    def sw_dash(self):
        self.stackedWidget.setCurrentIndex(0)
    def sw_subject(self):
        self.stackedWidget.setCurrentIndex(4)
    def sw_class(self):
        self.stackedWidget.setCurrentIndex(1)
    def sw_teachers(self):
        self.stackedWidget.setCurrentIndex(3)
    def sw_students(self):
        self.stackedWidget.setCurrentIndex(2)


    