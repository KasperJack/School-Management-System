import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt




class CreateAccount(QDialog):  
    def __init__(self):
        super().__init__()
        uic.loadUi('CreateAccount.ui', self)  # Load the .ui file



    









# Entry point of the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    window = CreateAccount()  # Create an instance of the Login class
    window.show()  # Show the window

    sys.exit(app.exec())  # Execute the application
