from PyQt6.QtWidgets import QApplication
import sys
from School_System.windows.login import Login

def run_app():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())

