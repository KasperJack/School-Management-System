
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QAbstractItemView, QHeaderView, QScrollArea, QVBoxLayout, QLabel, QTreeWidgetItem, QFileDialog, QSizePolicy,QGraphicsDropShadowEffect,QGraphicsBlurEffect,QTableWidget,QCalendarWidget,QTableView,QFrame
from PyQt6 import uic

from datetime import datetime
from PyQt6.QtGui import QIcon, QColor, QBrush, QPixmap, QPainter,QPainterPath,QTextCharFormat,QPen,QMouseEvent
from PyQt6.QtCore import pyqtSlot, QDate, Qt,QRect



#from School_System.helpers.db_utils import LOGGED_IN_USER_ID
#from School_System.helpers.db_utils import PROFILE_PIC
from School_System.windows.AddSubjectDialog import AddSubjectDialog
from School_System.windows.AddTeacherDialog import AddTeacherDialog
from School_System.windows.AddClassDialog import AddClassDialog
from School_System.windows.AddStudentDialog import AddStudentDialog
from School_System.windows.ViewClassDialog import ViewClassDialog
from School_System.windows.EditClassDialog import EditClassDialog
from School_System.windows.EditTeacherDialog import EditTeacherDialog
from School_System.windows.ExportPdfDialog import ExportPdfDialog
from School_System.windows.ExportExcelDialog import ExportExcelDialog
from School_System.windows.SettingsDialog import SettingsDialog
from School_System.windows.AddEventDialog import AddEventDialog

#from School_System.helpers.db_utils import * ?????
import School_System.helpers.db_utils as database
from School_System.ui import INDEX_SU ### ui file

from School_System.resources import  ICONS ,view_button_style_sheet ,edit_button_style_sheet,delete_button_style_sheet    #path to the Table Ionds directroy
import School_System.resources.qrc.rec_rc





class IndexSU(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(INDEX_SU, self)

        print(School_System.__version__)



        #print(database.LOGGED_IN_USER_ID)
        self.dashboard_s.clicked.connect(self.sw_dash)
        self.dashboard_b.clicked.connect(self.sw_dash)

        ###self.subject_s.clicked.connect(self.sw_subject)
        ###self.subject_b.clicked.connect(self.sw_subject)

        self.classes_s.clicked.connect(self.sw_class)
        self.classes_b.clicked.connect(self.sw_class)

        self.teachers_s.clicked.connect(self.sw_teachers)
        self.teachers_b.clicked.connect(self.sw_teachers)

        self.students_s.clicked.connect(self.sw_students)
        self.students_b.clicked.connect(self.sw_students)

        self.settings_b.clicked.connect(self.open_settings_dialog)
        self.settings_s.clicked.connect(self.open_settings_dialog)


        self.add_subject_button.clicked.connect(self.open_add_subject_dialog)
        self.add_class_button.clicked.connect(self.open_add_class_dialog)
        self.add_teacher_button.clicked.connect(self.open_add_teacher_dialog)
        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.add_event_button.clicked.connect(self.open_add_event_dialog)


        self.add_teacher_button_dash.clicked.connect(self.open_add_teacher_dialog)
        self.add_subject_button_dash.clicked.connect(self.open_add_subject_dialog)
        self.add_class_button_dash.clicked.connect(self.open_add_class_dialog)
        self.add_student_button_dash.clicked.connect(self.open_add_student_dialog)
        self.exportpdf.clicked.connect(self.open_export_pdf_dialog)
        self.exportexcel.clicked.connect(self.open_export_excel_dialog)

        self.logout_s.clicked.connect(self.logout)
        self.logout_b.clicked.connect(self.logout)
        self.students_table.cellClicked.connect(self.on_cell_clicked)
        self.profile_pic_user.clicked.connect(lambda: print("F"))

        #########################[search students table]################################
        self.search_bar.textChanged.connect(self.filter_students_table)
        self.class_combo_box.currentTextChanged.connect(self.filter_students_table)

        #################### update delete student tab  ##############################
        self.delete_s.clicked.connect(self.delete_student)
        self.modify_s.clicked.connect(self.modify_students_info_window)
        self.back_to_s_table.clicked.connect(self.sw_students)
        self.update_button.clicked.connect(self.update_student_info)
        self.update_pic.clicked.connect(self.open_image_dialog)
        self.hide_side_widget.clicked.connect(lambda:self.side_widget.hide()
)
        ################# closed windows ######################
        ##edit_class_dialog.finished.connect(self.dialog_closed)
        ##############################################################
        self.greet_user()
        self.update_on_start_up() #updates the counters
        self.setup_students_table()
        self.display_inactive_admins()
        self.setup_activity_log__table()
        # removes the seconds tab in the tab widget for admin access
        # self.tabWidget.removeTab(1)#################"

        self.display_last_entries()

        self.show_ids.stateChanged.connect(self.toggle_id_columns)
        self.filter_activity_type.currentIndexChanged.connect(self.apply_filters)
        self.filter_date.currentIndexChanged.connect(self.apply_filters)
        self.filter_user.currentIndexChanged.connect(self.apply_filters)
        self.filter_affected_entity.currentIndexChanged.connect(self.apply_filters)




        self.classes_table.verticalHeader().setVisible(False)

        self.classes_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.classes_table.setShowGrid(False)

        #self.classes_table.setSelectionBehavior(self.classes_table.SelectionBehavior.SelectRows)
        self.classes_table.setSelectionMode(self.classes_table.SelectionMode.NoSelection)
        self.classes_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)



        self.load_classes_table()
        #left Alignment for everything
        #self.classes_table.horizontalHeader().setDefaultAlignment(
            #Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)


        # auto adjust the size of the colusmns
        header = self.classes_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set specific columns to have a fixed size
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        #header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        #header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

        # Set the fixed size for these columns
        header.resizeSection(0, 45)
        #header.resizeSection(2, 70)
        #header.resizeSection(3, 80)
        header.resizeSection(6, 300)




        self.setup_teachers_scroll()
        self.search_edit_teachers.textChanged.connect(self.filter_teachers)


        #self.apply_floating_effect(self.icon_text)
        #self.apply_floating_effect(self.icon_only)
        self.apply_floating_effect(self.main_screen)
        self.apply_floating_effect(self.students_table)
        self.apply_floating_effect(self.search_bar)





        #blur_effect = QGraphicsBlurEffect()
        #blur_effect.setBlurRadius(2)  # Adjust the radius for more/less blur
        #self.icon_text.setGraphicsEffect(blur_effect)
        self.tabWidget_dash.setTabText(0, "Dash")
        self.tabWidget_dash.setTabText(1, "Admins")
        self.tabWidget_dash.setTabText(2, "Activity")

        self.setup_calendar()
        self.load_events()
        self.display_today_events()
        self.display_inactive_admins()
##################################################################################################################################
    def closeEvent(self, event):
        database.log_out()

    def greet_user(self):
        self.label_4.setText(f"{database.LOGGED_IN_USER_NAME}")

        if database.PROFILE_PIC:
            default_pixmap = QPixmap(f"{ICONS}/camu.jpg")
            # Get the button size and ensure it's square
            button_size = self.profile_pic_user.size()
            diameter = min(button_size.width(), button_size.height())

            # Create a new pixmap for the circular image
            circular_pixmap = QPixmap(diameter, diameter)
            circular_pixmap.fill(Qt.GlobalColor.transparent)  # Transparent background

            # Use QPainter to draw the circular image
            painter = QPainter(circular_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)  # Smooth transformation

            # Create a clipping path for the circle
            path = QPainterPath()
            path.addEllipse(0, 0, diameter, diameter)
            painter.setClipPath(path)

            # Draw the original pixmap scaled to fit within the circle
            scaled_pixmap = default_pixmap.scaled(
                diameter, diameter, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_pixmap)

            painter.end()

            # Set the circular pixmap as the button icon
            self.profile_pic_user.setIcon(QIcon(circular_pixmap))
            self.profile_pic_user.setIconSize(button_size)
            return


        default_pixmap = QPixmap(f"{ICONS}/profile_v.pnga")
        self.profile_pic_user.setIcon(QIcon(default_pixmap))






    def load_classes_student_search(self):
        self.class_combo_box.clear()
        self.class_combo_box.addItem("All Classes")
        self.class_combo_box.addItems(database.get_classes())



    def update_students_count(self):
        students = database.get_total_students()
        self.students_label.setText(f"Students | {students}")

    def update_teachers_count(self):
        teachers = database.get_total_teachers()
        self.teachers_label.setText(f"Teachers | {teachers}")

    def update_classes_count(self):
        classes = database.get_total_classes()
        self.classes_label.setText(f"Classes | {classes}")

    def update_on_start_up(self):
        self.update_classes_count()
        self.update_teachers_count()
        self.update_students_count()
        self.sw_dash()
        self.tabWidget_dash.setCurrentIndex(0)
        self.dashboard_b.setChecked(True)
        self.icon_only.setHidden(True)
        self.setStatusBar(None)
        self.side_widget.hide()







#################### inactive admins table ###########################


    def display_inactive_admins(self):
        # Create a container widget to hold all admin cards
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(10, 10, 10, 10)

        # Retrieve data from the database (assumes each row is a tuple: (full_name, email, registration_date))
        results = database.get_inactive_admins()

        # Create and add an AdminWidget for each inactive admin
        for admin in results:
            full_name, email, registration_date = admin
            admin_card = AdminWidget(self, full_name, email, registration_date)
            container_layout.addWidget(admin_card)

        container_layout.addStretch()  # Add stretch to push content to the top
        self.inactive_admins_scrollArea.setWidget(container)



    def activate_admin_t(self, full_name, email):
        confirmation = QMessageBox.question(
            self,
            "Confirm Activation",
            f"Are you sure you want to activate the admin:\n\nName: {full_name}\nEmail: {email}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            database.activate_admin(full_name, email)
            self.display_inactive_admins()  # Refresh the list





    def delete_admin_t(self, full_name, email):
        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the admin:\n\nName: {full_name}\nEmail: {email}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            database.delete_admin(full_name, email)
            self.display_inactive_admins()  # Refresh the list





#################### students table ##############################

    def setup_students_table(self):
        self.students_table.setSelectionBehavior(self.students_table.SelectionBehavior.SelectItems)
        self.students_table.setSelectionMode(self.students_table.SelectionMode.SingleSelection) ## only cells selection

        ### loads the students table
        self.load_students_to_table()
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.students_table.setSelectionMode(self.students_table.SelectionMode.NoSelection)


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
        self.students = database.get_students_info()  # Fetch the full dataset
        #self.display_students(self.students)
        self.filter_students_table()

    def display_students(self, students):
        """Display a given list of students in the table."""
        self.students_table.setRowCount(len(students))
        self.students_table.setColumnCount(8)
        self.students_table.setHorizontalHeaderLabels([
            "#", "Full Name", "Grade",
            "Class", "Birth Date", "Address", "Phone", "Email"
        ])

        for row_idx, student in enumerate(students):
            for col_idx, data in enumerate(student):
                item = QTableWidgetItem(str(data) if data is not None else "")
                self.students_table.setItem(row_idx, col_idx, item)

        for row in range(self.students_table.rowCount()):
            self.students_table.setRowHeight(row, 45)

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




    def on_cell_clicked(self, row=None, column=None):

        if row is None or column is None:
            sid = self.sid

        else:
            full_name_column = 1
            if column == full_name_column:
                id_column = 0
                id = self.students_table.item(row, id_column)
                name = self.students_table.item(row, full_name_column)
                sid = id.text()
                sname = name.text()
                self.sname = sname
                self.sid = sid
            else:
                return


        student_info = database.get_student_details(sid)
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

        if student_info['photo']:
            binary_data = student_info['photo']

            if isinstance(binary_data, str):
                binary_data = binary_data.encode('utf-8')

            pixmap = QPixmap()
            if pixmap.loadFromData(binary_data):
                # Set the QPixmap to a QLabel for display
                self.photo_label.setPixmap(pixmap)

        else:
            self.photo_label.setPixmap(QPixmap(f"{ICONS}/profile.png"))

        if not student_info['class_name']:
            self.s_class.setText("No class")
        else:
            self.s_class.setText(student_info['class_name'])

        stored_date = student_info['registration_date']
        date_object = datetime.strptime(stored_date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%d-%m-%Y")
        self.s_regestraion.setText(formatted_date)
        self.s_additional_info.setText(student_info['additional_info'])
        if row is not None or column is not None: self.side_widget.show()


    #################### update delete student tab  ##############################

    def delete_student(self):

        database.delete_student(self.sid,self.sname)
        self.load_students_to_table()
        self.update_students_count()
        self.refresh_setup_activity_log__table()
        self.side_widget.hide()



        #log_activity(activity_type,affected_entity,entity_name,entity_id,additional_info)

        ## add confermation  before deletion


    def  modify_students_info_window(self):

        student_info = database.get_student_details(self.sid)


        full_name = student_info['full_name']
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1]
        self.update_f_name.setText(first_name)
        self.update_l_name.setText(last_name)
        self.update_phone.setText(student_info['phone'])
        self.update_email.setText(student_info['email'])

        Bdate = student_info['birth_date']
        date = QDate.fromString(Bdate, "dd-MM-yyyy")
        self.update_bd.setDate(date)



        self.update_address.setText(student_info['address'])
        #self.s_class.setText(student_info['class_name'])
        self.update_additional_info.setText(student_info['additional_info'])

        self.comboBox_class.clear()

        if  student_info['class_name']:

            classes = database.get_classes_ids()
            for class_id, class_name in classes:
                self.comboBox_class.addItem(class_name, class_id)
            for index in range(self.comboBox_class.count()):
                item_text = self.comboBox_class.itemText(index)
                if item_text == student_info['class_name']:
                    self.comboBox_class.setItemData(index, QBrush(QColor(0, 120, 212)), Qt.ItemDataRole.BackgroundRole)
                    self.comboBox_class.setCurrentIndex(index)
        else:
            self.comboBox_class.addItem("NO class")
            classes = database.get_classes_ids()
            for class_id, class_name in classes:
                self.comboBox_class.addItem(class_name, class_id)  # Add class_name with class_id as userData


        if student_info['photo']:
            binary_data = student_info['photo']

            if isinstance(binary_data, str):
                binary_data = binary_data.encode('utf-8')

            pixmap = QPixmap()
            if pixmap.loadFromData(binary_data):
                # Set the QPixmap to a QLabel for display
                self.update_photo_la.setPixmap(pixmap)

        else:
            self.update_photo_la.setPixmap(QPixmap(f"{ICONS}/profile.png"))


        self.sw_mod_student()


        #### clear the box after

    def update_student_info(self):

        name = self.update_f_name.text()
        last_name = self.update_l_name.text()
        full_name = f"{name} {last_name}"



        if not hasattr(self, 'image_bin'):
            new_data = {
                "full_name": full_name,
                "birth_date": self.update_bd.date().toString("dd-MM-yyyy"),
                "phone": self.update_phone.text(),
                "email": self.update_email.text(),
                "address": self.update_address.text(),
                "additional_info": self.update_additional_info.toPlainText(),
                "class_id": None if self.comboBox_class.currentText() == "NO class" else self.comboBox_class.currentData(),
            }
            database.update_student_info(self.sid, full_name, new_data)
            self.load_students_to_table()
            self.refresh_setup_activity_log__table()
            self.sw_students()
            self.on_cell_clicked()
            return




        new_data = {
            "photo": None if self.image_bin is None else self.image_bin,
            "full_name": full_name,
            "birth_date": self.update_bd.date().toString("dd-MM-yyyy"),
            "phone": self.update_phone.text(),
            "email": self.update_email.text(),
            "address": self.update_address.text(),
            "additional_info": self.update_additional_info.toPlainText(),
            "class_id": None if self.comboBox_class.currentText() == "NO class" else self.comboBox_class.currentData(),
        }

        database.update_student_info(self.sid,full_name,new_data)
        self.load_students_to_table()
        self.refresh_setup_activity_log__table()
        self.on_cell_clicked()






    def open_image_dialog(self):
        # Open the file dialog
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",  # Starting directory
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"  # File filter
        )

        # Validate the file type
        if image_path and image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            with open(image_path, "rb") as file:
                binary_data = file.read()
            self.image_bin = binary_data



            if isinstance(binary_data, str):
                binary_data = binary_data.encode('utf-8')

            pixmap = QPixmap()
            if pixmap.loadFromData(binary_data):
                 # Set the QPixmap to a QLabel for display
                self.update_photo_la.setPixmap(pixmap)






        else:
            self.image_bin = None
            self.update_photo_la.setPixmap(QPixmap(f"{ICONS}/profile.png"))



    ################################### activity log table  ###########################

    def setup_activity_log__table(self):

        self.activity_log_table.verticalHeader().setVisible(False)
        self.activity_log_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


        self.log_data = database.get_activity_log()
        self.populate_filters()
        self.load_filtered_data_to_table(self.log_data)


        header = self.activity_log_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(8, 30)  # info coulmn

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 50)  ### log id

        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 50)  ### admin id

        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(7, 50)  # entity id







    def load_filtered_data_to_table(self,data):
        data.reverse() ## reverse the data direction
        # Set up the table
        self.activity_log_table.setRowCount(len(data))
        self.activity_log_table.setColumnCount(9)  # Original columns without the Label
        self.activity_log_table.setHorizontalHeaderLabels([
            "#", "Timestamp", "User ID", "User Name",
            "Activity Type", "Affected Entity", "Entity Name", "Entity ID", "?"
        ])



        # Hide ID columns (Log ID, User ID, and Entity ID)
        self.activity_log_table.setColumnHidden(0, True)  # Hide "Log ID" column
        self.activity_log_table.setColumnHidden(2, True)  # Hide "User ID" column
        self.activity_log_table.setColumnHidden(7, True)  # Hide "Entity ID" column


        # Load icons for each activity type
        add_icon = QIcon(f"{ICONS}/add.png")
        delete_icon = QIcon(f"{ICONS}/del.png")
        update_icon = QIcon(f"{ICONS}/update.png")
        info_icon =  QIcon(f"{ICONS}/info.png")
        # Populate the table
        for row_idx, row in enumerate(data):
            # Set the row color and icon based on activity_type
            activity_type = row[4]  # Assuming activity_type is the 5th column in the data
            row_color = None
            icon = update_icon  # Default icon

            if activity_type == "add":
                row_color = QColor(200, 255, 200)
                icon = add_icon
            elif activity_type == "delete":
                row_color = QColor(255, 200, 200)
                icon = delete_icon
            else:
                row_color = QColor(255, 255, 200)



            # Format the timestamp
            timestamp = row[1]  # Timestamp is at index 1
            try:
                timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Convert string to datetime object
                formatted_timestamp = timestamp_obj.strftime('%b %d, %H:%M:%S')  # Format as "Jan 11, 17:25:11"
            except ValueError:
                formatted_timestamp = timestamp  # Fallback if the timestamp is not in the expected format



            # Populate each column
            for col_idx, value in enumerate(row):
                if col_idx == 1:
                    # Use the formatted timestamp for column 1
                    table_item = QTableWidgetItem(formatted_timestamp)
                else:
                    # Otherwise, use the original value
                    table_item = QTableWidgetItem(str(value))

                # Set icon for the activity_type column
                if col_idx == 4:  # Adjust the index for your activity_type column
                    table_item.setIcon(icon)

                # Apply color to the row
                table_item.setBackground(row_color)
                # table_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                self.activity_log_table.setItem(row_idx, col_idx, table_item)  # Directly populate without the "+ 1"


            icon = info_icon
            # Create an item for the last column (icon column)
            icon_item = QTableWidgetItem()
            icon_item.setIcon(icon)
            icon_item.setBackground(row_color)  # Apply the row color to the icon column
            self.activity_log_table.setItem(row_idx, 8, icon_item)  # Set icon in the last column (index 8)



    def toggle_id_columns(self, state):
        show = state == 2
        #print(show)#debugging
        self.activity_log_table.setColumnHidden(0, not show)
        self.activity_log_table.setColumnHidden(2, not show)
        self.activity_log_table.setColumnHidden(7, not show)





    def populate_filters(self):

        self.filter_activity_type.clear()
        self.filter_date.clear()
        self.filter_user.clear()
        self.filter_affected_entity.clear()

        dates = set(row[1][:10] for row in self.log_data)
        users = set(row[3] for row in self.log_data)
        entities = set(row[5] for row in self.log_data)
        activity_types = set(row[4] for row in self.log_data)

        # Populate combo boxes with unique values
        self.filter_date.addItem("All")
        self.filter_date.addItems(sorted(dates))

        self.filter_user.addItem("All")
        self.filter_user.addItems(sorted(users))

        self.filter_affected_entity.addItem("All")
        self.filter_affected_entity.addItems(sorted(entities))

        self.filter_activity_type.addItem("All")
        self.filter_activity_type.addItems(sorted(activity_types))




    def apply_filters(self):
        # Get the selected values from the combo boxes
        selected_date = self.filter_date.currentText()
        selected_user = self.filter_user.currentText()
        selected_entity = self.filter_affected_entity.currentText()
        selected_activity_type = self.filter_activity_type.currentText()

        filtered_data = []
        for row in self.log_data:
            timestamp = row[1]
            user_name = row[3]
            affected_entity = row[5]
            activity_type = row[4]

            # Apply filters only if the respective value is not "All"
            if (selected_date == "All" or selected_date in timestamp) and \
                    (selected_user == "All" or selected_user == user_name) and \
                    (selected_entity == "All" or selected_entity == affected_entity) and \
                    (selected_activity_type == "All" or selected_activity_type == activity_type):
                filtered_data.append(row)

        filtered_data.reverse()
        self.load_filtered_data_to_table(filtered_data)

    def refresh_setup_activity_log__table(self):
        self.log_data = database.get_activity_log()
        self.populate_filters()
        self.load_filtered_data_to_table(self.log_data)




    def load_classes_table(self):

        results = database.get_classes_info()
        info_icon =  QIcon(f"{ICONS}/user.png")

        # Set up the table widget for 3 columns
        self.classes_table.setRowCount(len(results))  # Set rows based on query result count
        self.classes_table.setColumnCount(7)  # Set columns for "Full Name", "Email", "Registration Date"
        #self.classes_table.setHorizontalHeaderLabels(["id", "class", "Grade", "session","Date","students","Action"])

        header_labels = ["#", "class", "Grade", "session", "Date", "students", "Action"]
        for col_index, label in enumerate(header_labels):
            header_item = QTableWidgetItem(label)
            if col_index == 6:  # Example: Center alignment for the first column
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            else:  # Left alignment for other columns
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.classes_table.setHorizontalHeaderItem(col_index, header_item)






        for row_index, row_data in enumerate(results):
            for col_index, data in enumerate(row_data):
                # Check if it's the column where you want the icon and text, handle None by just using the icon if needed
                if col_index == 5:  # Assuming column 5 is for the students' data
                    icon_item = QTableWidgetItem()
                    if data:
                        icon_item.setText(str(data))  # Set the text if data exists
                    icon_item.setIcon(info_icon)  # Always set the icon
                    self.classes_table.setItem(row_index, col_index, icon_item)
                else:
                    item = QTableWidgetItem(str(data) if data is not None else "")
                    self.classes_table.setItem(row_index, col_index, item)


            # Add the "Actions" buttons
            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")
            view_button = QPushButton("view")


            edit_button.setStyleSheet(edit_button_style_sheet)
            delete_button.setStyleSheet(delete_button_style_sheet)
            view_button.setStyleSheet(view_button_style_sheet)


            #button_size = 30  # Set the desired size (e.g., 40x40)
            #edit_button.setFixedSize(button_size, button_size)
            #delete_button.setFixedSize(button_size, button_size)
            #view_button.setFixedSize(button_size, button_size)



            edit_button.clicked.connect(lambda _, r=row_index: self.edit_class(r))
            delete_button.clicked.connect(lambda _, r=row_index: self.delete_class(r))
            view_button.clicked.connect(lambda _, r=row_index: self.view_class(r))

            # Add buttons to a layout
            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(view_button)
            button_layout.addWidget(delete_button)


            # Create a widget to hold the buttons
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # Add the widget to the table
            self.classes_table.setCellWidget(row_index, 6, button_widget)

        for row in range(self.classes_table.rowCount()):
            self.classes_table.setRowHeight(row, 45)




    def edit_class(self, row_index):
        id_item = self.classes_table.item(row_index, 0)
        class_id = id_item.text()
        self.open_edit_class_dialog(class_id)


    def delete_class(self, row_index):
        id_item = self.classes_table.item(row_index, 0)
        class_id = id_item.text()
        print(class_id)


    def view_class(self, row_index):
        id_item = self.classes_table.item(row_index, 0)
        class_id = id_item.text()
        self.open_view_class_dialog(class_id)





    def setup_calendar(self):
        self.calendar = CustomCalendarWidget(self)

        layout = QVBoxLayout(self.cal_widget)  # or another layout type you're using
        layout.addWidget(self.calendar)
        #self.calendar.setShowWeekNumbers(False)
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        # Enable grid


        self.calendar.setStyleSheet("""  QCalendarWidget {
                background-color: #E3E3E3;  /* Light gray background */
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #FFFFFF;
            }
            QCalendarWidget QToolButton {
                background-color: #1E3A8A; /* Dark blue header */
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #122659;
            }
            QCalendarWidget QTableView {
                border: none;
                background-color: white;
            }
            QCalendarWidget QHeaderView {
                background-color: white;
                color: black;
                font-weight: bold;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
                font-size: 15px;
                selection-background-color: transparent;
                selection-color: black;
            }
                        /* Full header (Month/Year + Weekday names) */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #1E3A8A; /* Dark blue full header */
                color: white;
                border-radius: 0px;
            }
            QCalendarWidget QHeaderView {
                gridline-color: transparent;
                border: none;
    }
            
            """)

        # If you want to set cal_widget as the main widget
        #self.setCentralWidget(self.cal_widget)
        #self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

    def display_today_events(self):
        """Fetch and display today's events in a QTextEdit with formatting."""
        today = QDate.currentDate()
        events = [(event.title, event.color) for date, event in database.get_events() if date == today]

        if events:
            formatted_text = "<h2>📅 Events for Today</h2><ul>"
            for title, color in events:
                color_hex = color.name()  # Convert QColor to hex string
                formatted_text += f'<li><span style="color:{color_hex}; font-weight:bold;">{title}</span> - <i>No description</i></li>'
            formatted_text += "</ul>"
        else:
            formatted_text = "<p><i>No events for today.</i></p>"

        self.todays_events.setHtml(formatted_text)




    def display_last_entries(self):
        """Fetch and display the last 6 entry log records in a QTextEdit with formatting."""
        # Assume you have a function in your database module that returns the last 6 entries:
        # Each entry is a tuple: (id, name, email, role, timestamp, action)
        last_entries = database.get_last_entries()  # or get_last_six_entries()

        if last_entries:
            formatted_text = "<h2>📋 Last 6 Entry Log</h2>"
            # Build a table for a clear, tabular display
            formatted_text += """
            <table border="1" cellspacing="0" cellpadding="4" style="border-collapse: collapse; width: 100%;">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Timestamp</th>
                    <th>Action</th>
                </tr>
            """
            # Loop through each entry, ignoring the email (3rd field)
            for entry in last_entries:
                id, name, _, role, timestamp, action = entry
                formatted_text += f"""
                <tr>
                    <td>{id}</td>
                    <td>{name}</td>
                    <td>{role}</td>
                    <td>{timestamp}</td>
                    <td>{action}</td>
                </tr>
                """
            formatted_text += "</table>"
        else:
            formatted_text = "<p><i>No entry logs available.</i></p>"

        # Set the HTML content of your QTextEdit widget
        self.entry_log_text_edit.setHtml(formatted_text)




    def load_events(self):

        self.calendar.clear_events()

        events = database.get_events()

        # Add each event to the calendar
        for event_date, event in events:
            self.calendar.add_event(event_date, event)



        #####################################[switching]#############################################
        

    def open_add_subject_dialog(self):
        add_subject_dialog = AddSubjectDialog(self)
        add_subject_dialog.exec()
    def open_add_teacher_dialog(self):
        add_teacher_dialog = AddTeacherDialog(self)
        add_teacher_dialog.exec()
    def open_add_class_dialog(self):
        add_class_dialog = AddClassDialog(self)
        add_class_dialog.exec()
    def open_add_student_dialog(self):
        add_student_dialog = AddStudentDialog(self)
        add_student_dialog.exec()
    def open_view_class_dialog(self ,class_id):
        view_class_dialog = ViewClassDialog(self, class_id)
        view_class_dialog.exec()

    def open_edit_class_dialog(self, class_id):
        edit_class_dialog = EditClassDialog(self, class_id)
        edit_class_dialog.finished.connect(self.edit_class_dialog_closed)
        edit_class_dialog.exec()


    def open_add_event_dialog(self):
        add_event_dialog = AddEventDialog(self,database.LOGGED_IN_USER_ID)
        add_event_dialog.exec()


    def open_export_pdf_dialog(self):
        export_pdf_dialog = ExportPdfDialog(self)
        export_pdf_dialog.exec()

    def open_export_excel_dialog(self):
        export_excel_dialog = ExportExcelDialog(self)
        export_excel_dialog.exec()

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self,database.LOGGED_IN_USER_ID)
        settings_dialog.exec()



    def open_edit_teacher_dialog(self, teacher_id):
        edit_teacher_dialog = EditTeacherDialog(self, teacher_id)
        edit_teacher_dialog.exec()


    def edit_class_dialog_closed(self):
        #print("Dialog closed")#debugging
        edit_class_dialog = self.sender()

        if edit_class_dialog.is_modified:
            self.load_classes_table()
            # self.update_classes_count()
            self.load_classes_student_search()
            # self.index_instance.refresh_setup_activity_log__table()
            self.load_students_to_table()




    def logout(self):

        confirmation = QMessageBox.question(
            self,
            "logou ?",
            f"Are you sure you want to logout",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:

            from School_System.windows.login import Login
            self.close()
            database.reset()
            if not hasattr(self, 'login_window') or self.login_window is None:
                self.login_window = Login()
            self.login_window.show()







    def sw_dash(self):
        self.stackedWidget.setCurrentIndex(0)
    def sw_subject(self):
        self.stackedWidget.setCurrentIndex(6)
    def sw_class(self):
        self.stackedWidget.setCurrentIndex(1)
    def sw_teachers(self):
        self.stackedWidget.setCurrentIndex(3)
    def sw_students(self):
        self.stackedWidget.setCurrentIndex(2)
    def sw_more_about_s(self):
        self.stackedWidget.setCurrentIndex(4)
    def sw_mod_student(self):
        self.stackedWidget.setCurrentIndex(5)








    def setup_teachers_scroll(self):
        self.scrollArea_teachers.setWidgetResizable(True)
        self.scrollArea_teachers.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_teachers.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


        # Store the original data for reuse
        self.teachers_data = database.get_teachers_data()

        # Initial display of teachers
        self.display_teachers(self.teachers_data)





    def filter_teachers(self, search_text):
        # Filter teachers based on search text
        filtered_data = [
            teacher for teacher in self.teachers_data
            if search_text.lower() in teacher["name"].lower()
               and teacher["teacher_id"] != 62  # Keep your existing filter
        ]

        # Clear and redisplay teachers
        self.display_teachers(filtered_data)


    def apply_floating_effect(self, widget):
        # Create a subtle shadow effect
        shadow_effect = QGraphicsDropShadowEffect()

        # Make the shadow effect more subtle
        shadow_effect.setBlurRadius(5)  # Reduced blur radius for a softer shadow
        shadow_effect.setOffset(1, 1)  # Reduced offset for a minimal floating effect
        shadow_effect.setColor(QColor(0, 0, 0, 50))  # Lighter shadow color (lower alpha for subtlety)

        # Apply the effect to the widget
        widget.setGraphicsEffect(shadow_effect)

        # Optional: Slightly raise the widget to enhance the floating effect
        widget.move(widget.x(), widget.y() - 4)  # Raise it just a bit











    def display_teachers(self, data):
        # Configure scroll area


        # Container widget inside the scroll area
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Setup layout
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setSpacing(10)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add multiple TeacherWidget instances dynamically
        for teacher in data:
            if teacher["teacher_id"] == 62:
                continue
            teacher_widget = TeacherWidget(
                self,
                name=teacher["name"],
                subjects=teacher["subjects"],
                classes=teacher["classes"],
                teacher_id=teacher["teacher_id"]
            )
            scroll_layout.addWidget(teacher_widget)

        # Add a spacer to push content up if fewer widgets
        scroll_layout.addStretch()

        # Set container as the widget for the scroll area
        self.scrollArea_teachers.setWidget(container)


class TeacherWidget(QWidget):
    """A refined teacher card with tag-style subjects and classes, plus an icon next to the teacher's name.
       Displays a placeholder for subjects or classes if none are provided.
    """

    def __init__(self, parent, name, subjects, classes, teacher_id):
        super().__init__(parent)
        self.parent = parent
        self.teacher_id = teacher_id
        self.setupUI(name, subjects, classes)

    def setupUI(self, name, subjects, classes):
        # Use a QFrame to create a card-like container
        self.frame = QFrame(self)
        self.frame.setObjectName("cardFrame")
        self.frame.setStyleSheet("""
            QFrame#cardFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #F0F0F0);
                border: 1px solid #CCCCCC;
                border-radius: 10px;
            }
        """)

        # Layout for the card content with internal padding
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)  # Internal padding for the text
        frame_layout.setSpacing(10)

        # Teacher name row: icon and name
        name_layout = QHBoxLayout()
        # Load the icon (make sure ICONS is defined with your icons path)
        test_icon = QIcon(f"{ICONS}/user.png")
        icon_label = QLabel(self.frame)
        # Set the icon pixmap with a desired size (e.g., 40x40)
        icon_label.setPixmap(test_icon.pixmap(35, 35))
        name_layout.addWidget(icon_label)

        # Teacher name label
        name_label = QLabel(name, self.frame)
        name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        frame_layout.addLayout(name_layout)

        # Subjects row using a horizontal layout with tag-style labels
        subjects_layout = QHBoxLayout()
        subjects_indicator = QLabel("Subjects:", self.frame)
        subjects_indicator.setStyleSheet("font-size: 18px; color: #007ACC; font-weight: bold;")
        subjects_layout.addWidget(subjects_indicator)
        # Create a tag for each subject; if none, display a placeholder
        if subjects:
            for subject in subjects:
                subject_tag = QLabel(subject, self.frame)
                subject_tag.setStyleSheet("""
                    background-color: #E0F7FA;
                    color: #007ACC;
                    border: 1px solid #007ACC;
                    border-radius: 5px;
                    padding: 2px 6px;
                    font-size: 16px;
                """)
                subjects_layout.addWidget(subject_tag)
        else:
            no_subjects = QLabel("-no subjects-", self.frame)
            no_subjects.setStyleSheet("font-size: 16px; color: gray; font-style: italic;")
            subjects_layout.addWidget(no_subjects)
        subjects_layout.addStretch()  # Push content to the left
        frame_layout.addLayout(subjects_layout)

        # Classes row using a horizontal layout with tag-style labels
        classes_layout = QHBoxLayout()
        classes_indicator = QLabel("Classes:", self.frame)
        classes_indicator.setStyleSheet("font-size: 18px; color: #D35400; font-weight: bold;")
        classes_layout.addWidget(classes_indicator)
        # Create a tag for each class; if none, display a placeholder
        if classes:
            for cls in classes:
                class_tag = QLabel(cls, self.frame)
                class_tag.setStyleSheet("""
                    background-color: #FFF3E0;
                    color: #D35400;
                    border: 1px solid #D35400;
                    border-radius: 5px;
                    padding: 2px 6px;
                    font-size: 16px;
                """)
                classes_layout.addWidget(class_tag)
        else:
            no_classes = QLabel("-no classes-", self.frame)
            no_classes.setStyleSheet("font-size: 16px; color: gray; font-style: italic;")
            classes_layout.addWidget(no_classes)
        classes_layout.addStretch()  # Push content to the left
        frame_layout.addLayout(classes_layout)

        # Bottom layout for the edit button aligned to the right
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        edit_button = QPushButton("Edit", self.frame)
        edit_button.setFixedSize(90, 35)
        edit_button.setStyleSheet("""
QPushButton {
    background-color: #5E81AC; /* Nord Blue */
    color: #ECEFF4; /* Light text */
    border: 1px solid #81A1C1; /* Lighter blue border */
    border-radius: 0px; /* No roundness */
    padding: 6px 12px;
    font-family: "Segoe UI";
    font-size: 15px;
border-radius: 5px;

}

/* Hover State */
QPushButton:hover {
    background-color: #81A1C1; /* Lighter Nord Blue */
    border: 1px solid #88C0D0; /* Teal highlight */
}

/* Pressed State */
QPushButton:pressed {
    background-color: #4C566A; /* Darker Nord Blue */
    border: 1px solid #8FBCBB; /* Teal accent */
}

/* Edit Button Specific Style */
QPushButton#editButton {
    background-color: #88C0D0; /* Soft Teal Blue */
    color: #2E3440; /* Darker text for contrast */
    border: 1px solid #8FBCBB; /* Teal border */
}

QPushButton#editButton:hover {
    background-color: #8FBCBB; /* Slightly lighter teal */
    border: 1px solid #81A1C1; /* Soft blue highlight */
}

QPushButton#editButton:pressed {
    background-color: #5E81AC; /* Dark Nord Blue */
    border: 1px solid #4C566A; /* Darker border */
}

        """)
        edit_button.clicked.connect(self.on_button_click)
        bottom_layout.addWidget(edit_button)
        frame_layout.addLayout(bottom_layout)

        # Set the overall layout for the widget to include the card frame
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)  # Minimal outer margin
        outer_layout.addWidget(self.frame)

    def on_button_click(self):
        self.parent.open_edit_teacher_dialog(self.teacher_id)


#class ComboDelegate(QStyledItemDelegate):
#    def __init__(self, selected_class):
#        super().__init__()
#        self.selected_class = selected_class  # The current class name to compare
#
#    def paint(self, painter, option, index):
#        pass



class Event:
    def __init__(self, title, color=QColor(255, 100, 100, 180)):
        self.title = title
        self.color = color



class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Dictionary mapping QDate to a list of events
        self.events = {}

    def add_event(self, date: QDate, event):
        """Add an event to a specific date."""
        if date not in self.events:
            self.events[date] = []
        self.events[date].append(event)
        self.update()  # Repaint the calendar

    def clear_events(self):
        """Remove all events from the calendar."""
        self.events.clear()
        self.update()  # Repaint the calendar

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        if date in self.events:
            painter.save()

            painter.fillRect(rect, QColor("white"))

            date_text = str(date.day())
            date_rect = QRect(rect.left() + 2, rect.top() + 2, rect.width() - 4, 20)
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.drawText(date_rect, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft, date_text)

            events = self.events[date]
            current_y = date_rect.bottom() + 2
            event_card_height = 15
            spacing = 2

            #  each event stack
            for event in events:
                if current_y + event_card_height > rect.bottom() - 2:
                    break

                event_rect = QRect(rect.left() + 2, current_y, rect.width() - 4, event_card_height)
                painter.setBrush(event.color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(event_rect, 3, 3)


                painter.setPen(QPen(Qt.GlobalColor.black))
                painter.drawText(event_rect.adjusted(2, 0, -2, 0),
                                 Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                                 event.title)

                current_y += event_card_height + spacing

            painter.restore()
        else:

            painter.save()
            painter.fillRect(rect, QColor("white"))
            super().paintCell(painter, rect, date)
            painter.restore()


class AdminWidget(QWidget):
    """Custom widget to display an inactive admin in a card style."""

    def __init__(self, parent, full_name, email, registration_date):
        super().__init__(parent)
        self.parent = parent
        self.full_name = full_name
        self.email = email
        self.registration_date = registration_date
        self.setupUI()

    def setupUI(self):
        # Create a card container using QFrame with a subtle gradient and rounded corners
        self.frame = QFrame(self)
        self.frame.setObjectName("adminCard")
        self.frame.setStyleSheet("""
            QFrame#adminCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #F9F9F9);
                border: 1px solid #CCCCCC;
                border-radius: 10px;
            }
        """)

        # Layout for the card content with internal padding
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 20, 20, 20)
        frame_layout.setSpacing(10)

        # Full Name Label
        name_label = QLabel(self.full_name, self.frame)
        name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        frame_layout.addWidget(name_label)

        # Email Label
        email_label = QLabel(self.email, self.frame)
        email_label.setStyleSheet("font-size: 18px; color: #555555;")
        frame_layout.addWidget(email_label)

        # Registration Date Label
        reg_label = QLabel(f"Registered: {self.registration_date}", self.frame)
        reg_label.setStyleSheet("font-size: 16px; color: #777777;")
        frame_layout.addWidget(reg_label)

        # Action buttons layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push buttons to the right

        # Activate button
        activate_button = QPushButton("Activate", self.frame)
        activate_button.setFixedSize(90, 35)
        activate_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        activate_button.clicked.connect(self.activate)
        button_layout.addWidget(activate_button)

        # Delete button
        delete_button = QPushButton("Delete", self.frame)
        delete_button.setFixedSize(90, 35)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #ffcccc;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ffaaaa;
            }
        """)
        delete_button.clicked.connect(self.delete)
        button_layout.addWidget(delete_button)

        frame_layout.addLayout(button_layout)

        # Overall layout for this widget – add some outer margin if needed
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.frame)

    def activate(self):
        # Delegate activation to the parent widget
        self.parent.activate_admin_t(self.full_name, self.email)

    def delete(self):
        # Delegate deletion to the parent widget
        self.parent.delete_admin_t(self.full_name, self.email)
