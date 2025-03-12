from PyQt6.QtWidgets import QDialog, QMessageBox,QFileDialog,QHBoxLayout,QLabel
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import SETTINGS_DIALOG
from PyQt6.QtGui import QPixmap
from School_System.resources import  ICONS




class SettingsDialog(QDialog):
    def __init__(self, index_instance ,user_id= None ,parent=None):
        super().__init__(parent)
        uic.loadUi(SETTINGS_DIALOG, self)
        self.index_instance = index_instance  # main class instance
        self.user_id = user_id
        self.setWindowTitle("settings")
        self.populate_school_info()
        self.image_bin = None
        self.add_grades()
        self.add_sessions()



    def populate_school_info(self):
        school_info = database.get_school_data(1)


        if school_info[7]:
            binary_data = school_info[7]

            if isinstance(binary_data, str):
                binary_data = binary_data.encode('utf-8')

            pixmap = QPixmap()
            if pixmap.loadFromData(binary_data):
                # Set the QPixmap to a QLabel for display
                self.photo_label.setPixmap(pixmap)

        else:
            self.photo_label.setPixmap(QPixmap(f"{ICONS}/logo.png"))


        self.name_field.setText(school_info[1])
        self.address_field.setText(school_info[2])
        self.phone_field.setText(school_info[3])
        self.email_field.setText(school_info[4])
        self.director_field.setText(school_info[5])
        self.ecreated_field.setText(school_info[6])
        self.website_field.setText(school_info[8])
        self.description_field.setText(school_info[9])



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
                self.photo_label.setPixmap(pixmap)


        else:
            self.image_bin = None
            self.update_photo_la.setPixmap(QPixmap(f"{ICONS}/profile.png"))



    def update_info(self):
        pass



    def add_grades(self):
        grades = database.get_grades()

        # Create a horizontal layout for the frame
        layout = QHBoxLayout(self.frame)
        layout.setSpacing(10)  # Spacing between tags
        layout.setContentsMargins(10, 10, 10, 10)  # Optional margins

        # Create a tag for each grade with a refined style similar to TeacherWidget tags
        for grade in grades:
            label = QLabel(grade, self.frame)
            label.setStyleSheet("""
                background-color: #FCE4EC;   /* Soft background color */
                color: #AD1457;              /* Contrasting text color */
                border: 1px solid #AD1457;    /* Border with the same tone as text */
                border-radius: 5px;           /* Rounded corners */
                padding: 2px 6px;             /* Compact padding */
                font-size: 16px;              /* Consistent font size */
            """)
            layout.addWidget(label)

        self.frame.setLayout(layout)



    def add_sessions(self):
        sessions = database.get_sessions()

        # Create a horizontal layout for the frame
        layout = QHBoxLayout(self.frame_2)
        layout.setSpacing(10)  # Spacing between tags
        layout.setContentsMargins(10, 10, 10, 10)  # Optional margins

        # Create a tag for each grade with a refined style similar to TeacherWidget tags
        for session in sessions:
            label = QLabel(session, self.frame_2)
            label.setStyleSheet("""
                background-color: #FCE4EC;   /* Soft background color */
                color: #AD1457;              /* Contrasting text color */
                border: 1px solid #AD1457;    /* Border with the same tone as text */
                border-radius: 5px;           /* Rounded corners */
                padding: 2px 6px;             /* Compact padding */
                font-size: 16px;              /* Consistent font size */
            """)
            layout.addWidget(label)

        self.frame_2.setLayout(layout)
