import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic



class index(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('index.ui', self)

    
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = index()  # Create an instance of the Login class
    window.show()  # Show the window

    sys.exit(app.exec())  # Execute the application