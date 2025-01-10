import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, QScrollArea, QVBoxLayout, QLabel, QTreeWidgetItem
from PyQt6 import uic
from datetime import datetime
from PyQt6.QtGui import QIcon, QColor

from School_System.windows.AddSubjectDialog import AddSubjectDialog
from School_System.windows.AddTeacherDialog import AddTeacherDialog
from School_System.windows.AddClassDialog import AddClassDialog
from School_System.windows.AddStudentDialog import AddStudentDialog
import sqlite3
from School_System.db.dbio import connect

import School_System.resources.qrc.rec_rc
import School_System.resources.TableIcons
from School_System.helpers.db_utils import *

class indexSU(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'indexSU.ui')
        uic.loadUi(ui_path, self)

        #sbuttons#####
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
        self.add_subject_button.clicked.connect(self.open_add_subject_dialog)
        self.add_class_button.clicked.connect(self.open_add_class_dialog)
        self.add_teacher_button.clicked.connect(self.open_add_teacher_dialog)
        self.add_teacher_button_dash.clicked.connect(self.open_add_teacher_dialog)
        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.students_table.cellClicked.connect(self.on_cell_clicked)

        #########################[search students table]################################
        self.search_bar.textChanged.connect(self.filter_students_table)
        self.class_combo_box.currentTextChanged.connect(self.filter_students_table)

        #################### update delete student tab  ##############################
        self.delete_s.clicked.connect(self.delete_student)
        self.back_to_s_table.clicked.connect(self.sw_students)












        ##############################################################
        self.greet_user()
        self.update_on_start_up() #updates the counters
        self.setup_students_table()
        self.setup_inactive_admins_table()
        self.change_row_color(2, "red")
        # removes the seconds tab in the tab widget for admin access
        # self.tabWidget.removeTab(1)#################"



        self.activity_log_table.verticalHeader().setVisible(False)

        self.activity_log_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        io_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'TableIcons')
        print (io_path)

        self.load_data_to_table()









        self.scrollArea_teachers.setWidgetResizable(True)

        # Container widget inside the scroll area
        container = QWidget()
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setSpacing(10)

        # Add multiple TeacherWidget instances dynamically
        data = [
            {"name": "Teacher A", "subjects": ["Science", "Math", "Information"],
             "classes": ["class b01", "class b03", "class b05"]},
            {"name": "Teacher B", "subjects": ["English", "History"], "classes": ["class b02", "class b04"]},
            {"name": "Teacher C", "subjects": ["Physics", "Chemistry"], "classes": ["class b01", "class b06"]},
        ]
        for teacher in data:
            teacher_widget = TeacherWidget(
                name=teacher["name"],
                subjects=teacher["subjects"],
                classes=teacher["classes"]
            )
            scroll_layout.addWidget(teacher_widget)

        # Add a spacer to push content up if fewer widgets
        scroll_layout.addStretch()

        # Set container as the widget for the scroll area
        self.scrollArea_teachers.setWidget(container)


##################################################################################################################################


    def change_row_color(self, row_index, color):
        """
        Changes the background color of a specific row in the QTableWidget.

        Args:
            row_index (int): The row index of the row to change the color.
            color (str or QColor): The color to set for the row (can be a color name or QColor object).
        """
        # Check if the row_index is valid
        if row_index < 0 or row_index >= self.students_table.rowCount():
            print("Invalid row index")
            return

        # Create a QColor object if a string is passed
        if isinstance(color, str):
            color = QColor(color)

        # Loop through each column in the row
        for column in range(self.students_table.columnCount()):
            item = self.students_table.item(row_index, column)
            if item is None:
                # If the cell is empty, create a new item
                item = QTableWidgetItem()
                self.students_table.setItem(row_index, column, item)

            # Set the background color of the item
            item.setBackground(color)





    def greet_user(self):
        name = get_logged_in_user_name()
        self.label_user_name.setText(f"Hello, {name}")



    def load_classes_student_search(self):
        self.class_combo_box.addItems(get_classes())



    def update_students_count(self):
        students = get_total_students()
        self.students_label.setText(f"students | {students}")

    def update_teachers_count(self):
        teachers = get_total_teachers()
        self.teachers_label.setText(f"teachers | {teachers}")

    def update_classes_count(self):
        classes = get_total_classes()
        self.classes_label.setText(f"classes | {classes}")

    def update_on_start_up(self):
        self.update_classes_count()
        self.update_teachers_count()
        self.update_students_count()
        self.sw_dash()
        self.tabWidget_dash.setCurrentIndex(0)
        self.icon_only.setHidden(True)






#################### inactive admins table ###########################

    def setup_inactive_admins_table(self):
        self.inactive_admins_table.verticalHeader().setVisible(False)

        # prevents the table () from being edited
        self.inactive_admins_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.load_inactive_admins() ###load data
        header = self.inactive_admins_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row in range(self.inactive_admins_table.rowCount()):
            self.inactive_admins_table.setRowHeight(row, 40)



    def load_inactive_admins(self):
            
            results = get_inactive_admins()

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
                activate_button.clicked.connect(lambda _, r=row_index: self.activate_admin(r))
                delete_button.clicked.connect(lambda _, r=row_index: self.delete_admin(r))

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

    def activate_admin(self, row_index):
        full_name = self.inactive_admins_table.item(row_index, 0).text()
        email = self.inactive_admins_table.item(row_index, 1).text()

        confirmation = QMessageBox.question(
            self,
            "Confirm Activation",
            f"Are you sure you want to activate the user:\n\nName: {full_name}\nEmail: {email}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            activate_admin(full_name, email)
            self.load_inactive_admins()

    def delete_admin(self, row_index):
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
            delete_admin(full_name, email)
            self.load_inactive_admins()



#################### students table ##############################

    def setup_students_table(self):
        ### loads the students table
        self.load_students_to_table()## :load data
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.class_combo_box.addItem("All Classes")
        self.load_classes_student_search()
        # auto adjust the size of the colusmns
        header = self.students_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set specific columns to have a fixed size
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

        # Set the fixed size for these columns
        header.resizeSection(0, 45)
        header.resizeSection(2, 70)
        header.resizeSection(3, 80)
        header.resizeSection(4, 100)





    def load_students_to_table(self):
        """Load all students into the table."""
        self.students = get_students_info()  # Fetch the full dataset
        #self.display_students(self.students)
        self.filter_students_table()

    def display_students(self, students):
        """Display a given list of students in the table."""
        self.students_table.setRowCount(len(students))
        self.students_table.setColumnCount(8)
        self.students_table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Grade",
            "Class", "Birth Date", "Address", "Phone", "Email"
        ])

        for row_idx, student in enumerate(students):
            for col_idx, data in enumerate(student):
                item = QTableWidgetItem(str(data) if data is not None else "")
                self.students_table.setItem(row_idx, col_idx, item)

    def filter_students_table(self):
        """Filter the table based on the search input and selected class."""
        search_text = self.search_bar.text().strip().lower()
        selected_class = self.class_combo_box.currentText()

        # Filter based on class and search text
        filtered_students = self.students

        # If a specific class is selected, filter by class
        if selected_class != "All Classes":
            filtered_students = [
                student for student in filtered_students if student[3] == selected_class
            ]

        # Further filter by search text
        if search_text:
            filtered_students = [
                student for student in filtered_students if search_text in student[1].lower()
            ]

        self.display_students(filtered_students)

    def on_cell_clicked(self, row, column):
        full_name_column = 1
        if column == full_name_column:
            id_column = 0
            value = self.students_table.item(row, id_column)
            sid = value.text()
            student_info = get_student_details(sid)
            full_name = student_info['full_name']
            name_parts = full_name.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1]
            self.s_name.setText(first_name)
            self.s_last_name.setText(last_name)
            self.s_phone.setText(student_info['phone'])
            self.s_email.setText(student_info['email'])
            self.s_bd.setText(student_info['birth_date'])
            self.s_address.setText(student_info['address'])
            self.s_class.setText(student_info['class_name'])
            stored_date = student_info['registration_date']
            date_object = datetime.strptime(stored_date, "%Y-%m-%d")
            formatted_date = date_object.strftime("%d-%m-%Y")
            self.s_regestraion.setText(formatted_date)
            self.s_additional_info.setText(student_info['additional_info'])
            self.sw_more_about_s()


#################### update delete student tab  ##############################

    def delete_student(self):
        selected_indexes = self.students_table.selectedIndexes()

        row = selected_indexes[0].row()
        id_column = 0
        name_column = 1
        id_item = self.students_table.item(row, id_column)
        name_item = self.students_table.item(row, name_column)
        sid = id_item.text()
        sname = name_item.text()
        #print(sid,sname)
        delete_student(sid,sname)
        self.load_students_to_table()
        self.update_students_count()
        self.sw_students()

        #log_activity(activity_type,affected_entity,entity_name,entity_id,additional_info)
        ## add confermation  before deletion
################################### activity log table  ###########################



    def load_data_to_table(self):
        data = fetch_activity_log()  # Replace with your actual database path

        if isinstance(data, str):
            # If fetch_activity_log returned an error message
            print(f"Error: {data}")
            return

        # Set up the table
        self.activity_log_table.setRowCount(len(data))
        self.activity_log_table.setColumnCount(10)  # Original columns + Empty Label + Button
        self.activity_log_table.setHorizontalHeaderLabels([
            "Label", "Log ID", "Timestamp", "User ID", "User Name",
            "Activity Type", "Affected Entity", "Entity Name", "Entity ID", "Button"
        ])

        # Load icons
        add_icon = QIcon("./add.png")  # Replace with your icon paths
        delete_icon = QIcon("/home/kasper/projects/PYside6/test-app/School_System/ui/del.png")
        default_icon = QIcon("/home/kasper/projects/PYside6/test-app/School_System/ui/update.png")

        # Populate the table
        for row_idx, row in enumerate(data):
            # Set the row color and icon based on activity_type
            activity_type = row[4]  # Assuming activity_type is the 5th column in the data
            row_color = None
            icon = default_icon

            if activity_type == "add":
                row_color = QColor(200, 255, 200)  # Light green for "add"
                icon = add_icon
            elif activity_type == "delete":
                row_color = QColor(255, 200, 200)  # Light red for "delete"
                icon = delete_icon
            else:
                row_color = QColor(255, 255, 200)  # Light yellow for others

            # Populate each column
            for col_idx, value in enumerate(row):
                table_item = QTableWidgetItem(str(value))

                # Set icon for the activity_type column
                if col_idx == 4:  # Adjust the index for your activity_type column
                    table_item.setIcon(icon)

                # Apply color to the row
                table_item.setBackground(row_color)
                #table_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                self.activity_log_table.setItem(row_idx, col_idx + 1, table_item)

            # Add a button at the end
            button = QPushButton("Action")
            button.clicked.connect(
                lambda checked, r=row: self.handle_button_click(r))  # Pass the row data to the handler
            self.activity_log_table.setCellWidget(row_idx, 9, button)  # Column index for the button

    def handle_button_click(self, row_data):
        """
        Handles the button click for a specific row.

        Args:
            row_data (tuple): The data of the row where the button was clicked.
        """
        print(f"Button clicked for row: {row_data}")

        #####################################[switching]#############################################
        

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





    def sw_dash(self):
        self.stackedWidget.setCurrentIndex(0)
    def sw_subject(self):
        self.stackedWidget.setCurrentIndex(5)
    def sw_class(self):
        self.stackedWidget.setCurrentIndex(1)
    def sw_teachers(self):
        self.stackedWidget.setCurrentIndex(3)
    def sw_students(self):
        self.stackedWidget.setCurrentIndex(2)
    def sw_more_about_s(self):
        self.stackedWidget.setCurrentIndex(4)


class TeacherWidget(QWidget):
    """Custom widget to represent a teacher card."""

    def __init__(self, name, subjects, classes):
        super().__init__()

        # Set a layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5,5)
        layout.setSpacing(0)

        # Teacher's name and subjects
        teacher_label = QLabel(f"{name} ({', '.join(subjects)})")
        teacher_label.setStyleSheet("font-weight: bold; font-size: 25px;")
        layout.addWidget(teacher_label)

        # Classes
        classes_label = QLabel(" ".join(classes))
        classes_label.setStyleSheet("font-size: 16px; color: gray;")
        layout.addWidget(classes_label)

        # Add a button
        button = QPushButton("Button")
        button.setFixedSize(80, 30)
        button.setStyleSheet("background-color: lightgray;")

        # Add the button to a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        layout.addLayout(button_layout)

        # Set styling directly using setStyleSheet
        self.setStyleSheet("""
                    background-color: #ddd;
                    border-radius: 0px;
                    padding: 7px;
                """)
        self.setFixedHeight(125)  # Set height for consistent look
