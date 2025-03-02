
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QRadioButton, QPushButton, QDialog, QMessageBox,QAbstractItemView,QHeaderView,QLabel,QHBoxLayout,QVBoxLayout,QFrame,QButtonGroup,QGraphicsDropShadowEffect
from PyQt6 import uic
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import  QIcon,QColor


import School_System.helpers.db_utils as database
import School_System.helpers.strings as fmt
from School_System.ui import ADD_REMOVE_DB
from School_System.resources import  ICONS, delete_s_button_style_sheet


from School_System.db.DatabaseManager import db_manager_instance





class AddRemoveDB(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(ADD_REMOVE_DB, self)
        self.db_manager = db_manager_instance
        self.setWindowTitle("Add Database")

        self.add_db_button.clicked.connect(self.add_data_base)
        self.close_button.clicked.connect(self.close)
        self.populate_db_cards()


    def populate_db_cards(self):
        """Populate the scroll area with card widgets for each database."""
        db_files = self.db_manager.get_all_databases()



        current_dbs = [db for db in db_files if db.endswith("(current)")]
        non_current_dbs = [db for db in db_files if not db.endswith("(current)")]

        # If a current database exists, place it at the beginning:
        if current_dbs:
            ordered_db_files = current_dbs + non_current_dbs
        else:
            ordered_db_files = db_files




        #print(db_files)


        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(10, 10, 10, 10)

        # Create a QButtonGroup for the radio buttons.
        self.radio_group = QButtonGroup(self)
        self.radio_group.setExclusive(True)  # This is True by default.

        # Optionally, connect a signal to detect when a new button is selected.
        #self.radio_group.buttonClicked.connect(self.on_radio_button_clicked)

        # Create a card for each database file.
        for db_file in ordered_db_files:
            # Extract the database name by removing the extension and "(current)" indicator.
            db_name = db_file.replace(" (current)", "").replace(".db", "")
            is_current = db_file.endswith("(current)")
            card = DatabaseSelectionCard(
                parent=self,
                db_name=db_name,
                is_current=is_current,
                radio_callback=self.on_radio_button_toggled,
                delete_callback=self.delete_database
            )
            # Add the card's radio button to the group.
            self.radio_group.addButton(card.radio_button)
            container_layout.addWidget(card)

        container_layout.addStretch()  # Push cards to the top.
        self.db_scrollArea.setWidget(container)





    def on_radio_button_toggled(self, checked, db_name):
        """Handle the radio button toggle event."""
        if checked:

            #print(f"Selected Database: {db_name}")
            #self.db_manager.change_database(db_name)
            self.db_manager.change_database(db_name)
            database.update_route()
            #self.populate_db_selection()
        else:
            self.db_manager.change_database("null.db")





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
            self.populate_db_cards()








    def add_data_base(self):

        db_name = self.db_name.text()

        if not db_name:
            return
        """""
        for row in range(self.db_table.rowCount()):
            existing_db_name = self.db_table.item(row, 1).text()
            if existing_db_name == db_name:
                print("Database name already exists!")
                return """

        self.db_manager.create_new_db(db_name)
        self.populate_db_cards()









class DatabaseSelectionCard(QWidget):
    """A card-style widget for selecting a database with enhanced styling and custom radio button."""

    def __init__(self, parent, db_name, is_current, radio_callback, delete_callback):
        super().__init__(parent)
        self.db_name = db_name
        self.radio_callback = radio_callback  # Callback when radio toggled
        self.delete_callback = delete_callback  # Callback when delete is clicked
        self.is_current = is_current
        self.setupUI()

    def setupUI(self):
        # Create a card container using QFrame with a refined gradient and rounded corners.
        self.frame = QFrame(self)
        self.frame.setObjectName("dbCard")
        self.frame.setStyleSheet("""
            QFrame#dbCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #fdfdfd, stop:1 #f1f1f1);
                border: 1px solid #cccccc;
                border-radius: 10px;
            }
            QFrame#dbCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffffff, stop:1 #e8e8e8);
            }
        """)

        # Apply a drop shadow effect to the card.
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.frame.setGraphicsEffect(shadow)

        # Create a horizontal layout inside the card with internal padding.
        frame_layout = QHBoxLayout(self.frame)
        frame_layout.setContentsMargins(20, 10, 20, 10)
        frame_layout.setSpacing(15)

        # Radio button for selecting this database with a custom style.
        self.radio_button = QRadioButton(self.frame)
        self.radio_button.setChecked(self.is_current)
        self.radio_button.setStyleSheet("""
            QRadioButton {
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #cccccc;
                border-radius: 10px;
                background-color: #ffffff;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #007ACC;
                border-radius: 10px;
                background-color: #007ACC;
            }
        """)
        self.radio_button.toggled.connect(lambda checked: self.radio_callback(checked, self.db_name))
        frame_layout.addWidget(self.radio_button)

        # Label to display the database name.
        name_label = QLabel(self.db_name, self.frame)
        name_label.setStyleSheet("font-size: 20px; color: #333333;")
        frame_layout.addWidget(name_label)

        frame_layout.addStretch()  # Push the delete button to the far right.

        # Delete button with an icon.
        delete_button = QPushButton(self.frame)
        delete_button.setIcon(QIcon(f"{ICONS}/del.png"))
        delete_button.setIconSize(QSize(24, 24))
        delete_button.setFixedSize(40, 40)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #ffcccc;
                border-radius: 5px;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_callback(self.db_name))
        frame_layout.addWidget(delete_button)

        # Outer layout for this card widget to provide extra margin.
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.frame)
