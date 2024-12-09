import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, QScrollArea, QVBoxLayout, QLabel, QTreeWidgetItem
from PyQt6 import uic

from School_System.windows.AddSubjectDialog import AddSubjectDialog
from School_System.windows.AddTeacherDialog import AddTeacherDialog
from School_System.windows.AddClassDialog import AddClassDialog
from School_System.windows.AddStudentDialog import AddStudentDialog
import sqlite3
from School_System.db.dbio import connect

import School_System.resources.qrc.rec_rc
from School_System.helpers.db_utils import *
from School_System.windows.dbtest import students


class indexSU(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'indexSU.ui')
        uic.loadUi(ui_path, self)

        #side bar buttons#####"
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
        self.add_class_button.clicked.connect(self.open_add_class_dialog)
        self.add_teacher_button.clicked.connect(self.open_add_teacher_dialog)
        self.add_teacher_button_dash.clicked.connect(self.open_add_teacher_dialog)
        self.add_student_button.clicked.connect(self.open_add_student_dialog)

        #removes the seconds tab in the tab widget for admin access
        #self.tabWidget.removeTab(1)#################"


        self.icon_only.setHidden(True)
        self.inactive_admins_table.verticalHeader().setVisible(False)

        #prevents the table () from being edited
        self.inactive_admins_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        ### loads the students table
        self.load_students_to_table()
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        #header = self.students_table.horizontalHeader()
        #header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)



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
        self.update_students_count()


        self.load_inactive_users()

        #self.tableWidget.setColumnWidth(0,150)
        #self.tableWidget.setColumnWidth(1,150)
        #self.tableWidget.setColumnWidth(2,150)
        #self.tableWidget.setColumnWidth(3,150)
        # Set the height of all rows to 50 pixels

        header = self.inactive_admins_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row in range(self.inactive_admins_table.rowCount()):
            self.inactive_admins_table.setRowHeight(row, 40)








    def open_add_subject_dialog(self):
        # Create an instance of the AddSubjectDialog
        add_subject_dialog = AddSubjectDialog(self)
        add_subject_dialog.exec()

    def open_add_teacher_dialog(self):
        # Create an instance of the AddTeacherDialog
        add_teacher_dialog = AddTeacherDialog(self)
        add_teacher_dialog.exec()

    def open_add_class_dialog(self):
        add_class_dialog = AddClassDialog(self)
        add_class_dialog.exec()
    def open_add_student_dialog(self):
        add_student_dialog = AddStudentDialog(self)
        add_student_dialog.exec()




    def update_students_count(self):
        students = get_total_students()
        self.students_label.setText(f"students | {students}")




    def load_inactive_users(self):
            
            results = get_inactive_users()

            # Set up the table widget for 3 columns
            self.inactive_admins_table.setRowCount(len(results))  # Set rows based on query result count
            self.inactive_admins_table.setColumnCount(4)  # Set columns for "Full Name", "Email", "Registration Date"
            self.inactive_admins_table.setHorizontalHeaderLabels(["Full Name", "Email", "Registration Date", "Actions"])

            # Populate the table
            for row_index, row_data in enumerate(results):
                for col_index, data in enumerate(row_data):
                    self.inactive_admins_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))


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
                self.inactive_admins_table.setCellWidget(row_index, 3, button_widget)  # Column 3 is the "Actions" column

            #self.tableWidget.resizeColumnsToContents()

    def load_students_to_table(self):
        """Fetch student information and populate the students_table."""
        db_path = connect()

        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()
            # Query to get student info along with grade
            query = """
            SELECT 
                students.student_id,
                students.full_name,
                students.gender,
                grades.grade_name,
                students.class_name,
                students.birth_date,
                students.address,
                students.phone,
                students.email
            FROM 
                students
            LEFT JOIN 
                class ON students.class_name = class.class_name
            LEFT JOIN 
                grades ON class.grade_name = grades.grade_name
            """
            cursor.execute(query)
            students = cursor.fetchall()

        # Set up the table
        self.students_table.setRowCount(len(students))
        self.students_table.setColumnCount(9)
        self.students_table.setHorizontalHeaderLabels([
            "Student ID", "Full Name", "Gender", "Grade",
            "Class Name", "Birth Date", "Address", "Phone", "Email"
        ])

        # Populate the table
        for row_idx, student in enumerate(students):
            for col_idx, data in enumerate(student):
                item = QTableWidgetItem(str(data) if data is not None else "")
                self.students_table.setItem(row_idx, col_idx, item)



    # Methods to handle the buttons' functionality
    def activate_user(self, row_index):
        full_name = self.inactive_admins_table.item(row_index, 0).text()  # Get full_name from row
        email = self.inactive_admins_table.item(row_index, 1).text()  # Get email from row


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
        full_name = self.inactive_admins_table.item(row_index, 0).text()  # Get full_name from row
        email = self.inactive_admins_table.item(row_index, 1).text()  # Get email from row


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


    