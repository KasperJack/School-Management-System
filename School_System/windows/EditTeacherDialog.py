
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView, QHeaderView,QTreeWidget, QTreeWidgetItem,QMenu,QFrame,QListWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor ,QBrush,QIcon,QFont


import School_System.helpers.db_utils as database
from School_System.helpers.db_utils import add_teacher
from School_System.ui import EDIT_TEACHER_DIALOG
from School_System.resources import  ICONS
from School_System.resources import  ICONS

# best candidates ## book.png and 90Darrow.png

class EditTeacherDialog(QDialog):
    def __init__(self, index_instance, teacher_id=None, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance  #main class instance
        self.teacher_id = teacher_id
        uic.loadUi(EDIT_TEACHER_DIALOG, self)

        self.setWindowTitle("Edit Teacher")
        self.teacher_info()

        #self.tree_widget.setHeaderLabel("Adem Boubaker")  # Se
        self.tree_widget.setColumnCount(2)
        self.add_subjects()
        self.add_classes_and_grades()
        self.rearrange_tree()
        self.tree_widget.setColumnWidth(0, 200)
        self.tree_widget.setColumnWidth(1, 90)
        self.tree_widget.expandAll()
        self.update_info.clicked.connect(self.update_teacher_info)
        self.edit_button.clicked.connect(self.on_edit_press)
        self.undoo_button.clicked.connect(self.undo_changes)


##################################




















        #self.highlight_top_level_items()

        #self.tree_widget.setRootIsDecorated(True)  # Show expand/collapse icons and tree lines
        #self.tree_widget.setIndentation(20)

        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)






    def add_subjects(self):
        all_subjects = database.get_teacher_subjects(self.teacher_id)
        folder_icon = QIcon(f"{ICONS}/book.png")

        for subject_id, subject_name in all_subjects:
            subject_item = QTreeWidgetItem(self.tree_widget)
            subject_item.setText(0, subject_name)
            subject_item.setIcon(0, folder_icon)  # Set icon for the first column
            # Set the subject name

            # Store the subject ID in the item
            subject_item.setData(0, Qt.ItemDataRole.UserRole, subject_id)

            # Set the font to bold for parent items
            font = QFont()
            font.setBold(True)
            subject_item.setFont(0, font)  # Apply bold font to the parent item (subject)

            # If you want to make it dynamic, check if it has children (if applicable)
            if subject_item.childCount() > 0:
                subject_item.setFont(0, font)  # Make sure parent items are bold



    def add_classes_and_grades(self):
        test = database.get_teacher_classes(self.teacher_id)
        folder_icon = QIcon(f"{ICONS}/90Darrow.png")

        for subject_id, class_name, class_id, grade, ts_id in test:
            # Find the subject item by its ID
            subject_item = self.find_subject_item(subject_id)
            if subject_item:
                # Add the class and grade as a child item under the subject
                class_item = QTreeWidgetItem(subject_item)
                class_item.setText(0, class_name)
                class_item.setIcon(0, folder_icon)  # Set icon for the first column

                class_item.setText(1, grade)  # Set the grade in the third column

                # Store the class_id and ts_id in the item
                class_item.setData(0, Qt.ItemDataRole.UserRole, class_id)  # Store class_id
                class_item.setData(1, Qt.ItemDataRole.UserRole, ts_id)  # Store ts_id


    def find_subject_item(self, subject_id):
        # Find the subject item by its ID
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.data(0, Qt.ItemDataRole.UserRole) == subject_id:
                return item
        return None



    def show_context_menu(self, position: QPoint):
        # Get the item at the clicked position
        item = self.tree_widget.itemAt(position)

        if item:  # Only show the context menu if an item exists at the position
            # Create the context menu
            context_menu = QMenu(self)

            # Add actions to the menu
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")

            # Show the menu at the global position
            action = context_menu.exec(self.tree_widget.viewport().mapToGlobal(position))

            # Handle actions
            if action == edit_action:
                print("Edit action triggered")
                # Implement edit functionality
            elif action == delete_action:
                print("Delete action triggered")
                # Implement delete functionality






    def highlight_top_level_items(self):
        # Loop through all top-level items
        for i in range(self.tree_widget.topLevelItemCount()):
            top_item = self.tree_widget.topLevelItem(i)

            # Highlight only the top-level item
            for column in range(self.tree_widget.columnCount()):
                top_item.setBackground(column, QBrush(QColor(255, 230, 200)))  # Light orange background
                top_item.setForeground(column, QBrush(QColor(128, 0, 0)))



    def rearrange_tree(self):
        parent_items = []
        leaf_items = []

        # Separate parent and leaf items
        for i in range(self.tree_widget.topLevelItemCount() - 1, -1, -1):  # Iterate backward
            item = self.tree_widget.takeTopLevelItem(i)  #detach
            if item.childCount() > 0:
                parent_items.append(item)
            else:
                leaf_items.append(item)

        # Add parent items first
        for parent_item in parent_items:
            self.tree_widget.addTopLevelItem(parent_item)

        # Add leaf items at the bottom
        for leaf_item in leaf_items:
            self.tree_widget.addTopLevelItem(leaf_item)


    def teacher_info(self):

        self.update_info.hide()
        self.undoo_button.hide()

        teacher_info = database.get_teacher_info(self.teacher_id)
        self.tree_widget.setHeaderLabel(teacher_info[1])

        full_name = teacher_info[1] if teacher_info[1] else ""
        name_parts = full_name.split(" ", 1)

        # Assign first and last name safely
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        self.name_field.setText(first_name)
        self.last_name_field.setText(last_name)
        self.email_field.setText(teacher_info[3])
        self.phone_field.setText(teacher_info[2])
        self.address_field.setText(teacher_info[4])
        self.regestarion_date.setText(teacher_info[5])

        self.name_field.setReadOnly(True)
        self.last_name_field.setReadOnly(True)
        self.email_field.setReadOnly(True)
        self.phone_field.setReadOnly(True)
        self.address_field.setReadOnly(True)
        self.regestarion_date.setReadOnly(True)





    def on_edit_press(self):
        self.edit_button.hide()

        self.update_info.show()
        self.undoo_button.show()
        self.name_field.setReadOnly(False)
        self.last_name_field.setReadOnly(False)
        self.email_field.setReadOnly(False)
        self.phone_field.setReadOnly(False)
        self.address_field.setReadOnly(False)
        self.groupBox.setStyleSheet("""
QLineEdit {
    background-color: #eceff4; /* Light background */
    color: #000000; /* Black text */
    border: none; /* Remove default border */
    border-bottom: 1px solid #4C566A; /* Subtle bottom border */
    padding: 6px; /* Padding inside the field */
    outline: none; /* Remove focus outline */
}

/* Focused Input Field */
QLineEdit:focus {
    border-bottom: 2px solid #88C0D0; /* Thicker light blue bottom border on focus */
    background-color: #e1e9f2; /* Slightly lighter background on focus */
}

/* Placeholder Text */
QLineEdit::placeholder {
    color: #4C566A; /* Darker gray for placeholder text */
}

/* Label Style */
QLabel {
    color: #2e3440; /* Light text color */
    font-weight: bold; /* Bold text to emphasize the label */
    margin-top: 4px; /* Space between the label and the input field */
}

/* Optional: Focused Label Change (to match the input field) */
QLineEdit:focus + QLabel {
    color: #88C0D0; /* Change label color to light blue on focus */
}

""")





    def update_teacher_info(self):

        name = self.name_field.text()
        last_name = self.last_name_field.text()
        full_name = f"{name} {last_name}"
        phone = self.phone_field.text()
        email = self.email_field.text()
        address = self.address_field.text()

        if not name or not last_name or not phone or not email : return



        new_data = {
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "address": address,
        }




        self.tree_widget.setHeaderLabel(full_name)

        database.update_teacher_info(self.teacher_id,new_data)
        self.index_instance.setup_teachers_scroll()

        self.groupBox.setStyleSheet("""     QLineEdit {
        border: none;
    } """)
        self.name_field.setReadOnly(True)
        self.last_name_field.setReadOnly(True)
        self.email_field.setReadOnly(True)
        self.phone_field.setReadOnly(True)
        self.address_field.setReadOnly(True)
        self.regestarion_date.setReadOnly(True)
        self.update_info.hide()

        self.edit_button.show()

        self.update_info.hide()
        self.undoo_button.hide()



    def undo_changes(self):
        self.groupBox.setStyleSheet("""     QLineEdit {
              border: none;
          } """)
        self.edit_button.show()
        self.teacher_info()