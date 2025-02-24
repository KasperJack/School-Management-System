from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit,QGraphicsDropShadowEffect
from PyQt6 import uic
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from School_System.ui import LOGIN # ui file path
from School_System.windows.CreateAccountDialog import CreateAccountDialog
from School_System.windows.IndexSU import IndexSU
import School_System.helpers.db_utils as database
import School_System.resources.qrc.rec_rc




class Login(QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi(LOGIN, self)

        self.setWindowTitle("Login")
        self.login_button.clicked.connect(self.authenticate_user)
        self.create_account_button.clicked.connect(self.open_create_account_dialog)
        self.forget_password_button.clicked.connect(self.forget_password)
        #aself.view_password_button.clicked.connect(self.toggle_password_visibility)
        self.remember_me_button.toggled.connect(self.remember_me)
        self.apply_floating_effect(self.widget)
        #self.widget.setStyleSheet("background-color: white;")
        #self.setAutoFillBackground(True)



    def remember_me(self, checked):
        if checked:
            self.email_field.setText("Button is checked")
        else:
            self.email_field.setText("Button is unchecked")



    def forget_password(self):
        pass



    def open_create_account_dialog(self):
        # Create an instance of the CreateAccountDialog
        create_account_dialog = CreateAccountDialog(self)  
        create_account_dialog.exec()  






    def toggle_password_visibility(self):
        # Toggle the echoMode of the password field
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)




        

    def authenticate_user(self):
        # Get email and password from input fields
        email = self.email_field.text()
        password = self.password_field.text()

        # Validate inputs
        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Both email and password fields must be filled.")
            return
        
        evaluate = database.login_user(email,password)

        if evaluate == database.SUPERADMIN:
            QMessageBox.information(self, "superadmin",f"Welcome {database.LOGGED_IN_USER_NAME}")
            # Load the IndexSU window
            self.index_window = IndexSU()
            self.index_window.show()   
            self.close()    



        elif evaluate == database.ADMIN:
            QMessageBox.information(self, " admin",f"Welcome {database.LOGGED_IN_USER_NAME}")
            # Load the IndexSU window(for admins)
            self.index_window = IndexSU()
            self.index_window.show()
            self.close()


        elif evaluate == database.USER_INACTIVE:
            QMessageBox.critical(self, "Login Failed", f"account is inactive .")

        else:
            QMessageBox.critical(self, "Login Failed", "Invalid email or password. Please try again.")




##=========================================================##
##
##END ##
##
##=========================================================##        



    def apply_floating_effect(self, widget):
        # Create a subtle shadow effect
        shadow_effect = QGraphicsDropShadowEffect()

        # Make the shadow effect more subtle
        shadow_effect.setBlurRadius(8)  # Reduced blur radius for a softer shadow
        shadow_effect.setOffset(2, 2)  # Reduced offset for a minimal floating effect
        shadow_effect.setColor(QColor(0, 0, 0, 80))  # Lighter shadow color (lower alpha for subtlety)

        # Apply the effect to the widget
        widget.setGraphicsEffect(shadow_effect)

        # Optional: Slightly raise the widget to enhance the floating effect
        widget.move(widget.x(), widget.y() - 4)  # Raise it just a bit







