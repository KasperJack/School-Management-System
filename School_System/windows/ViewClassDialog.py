
from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import VIEW_CLASS_DIALOG


class ViewClassDialog(QDialog):
    def __init__(self, index_instance, parent=None):
        super().__init__(parent)
        self.index_instance = index_instance
        uic.loadUi(VIEW_CLASS_DIALOG, self)

        self.setWindowTitle("view Class")



        self.add_file.clicked.connect(self.open_image_dialog)

    def open_image_dialog(self):
        # Open the file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",  # Starting directory
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"  # File filter
        )

        # Validate the file type
        if file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"Valid image selected: {file_path}")
        else:
            print("Invalid file selected or canceled.")



        

