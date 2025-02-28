from School_System.db.DatabaseManager import db_manager_instance

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit,QGraphicsDropShadowEffect
from PyQt6 import uic
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from School_System.ui import LOGIN # ui file path

from School_System.windows.CreateAccountDialog import CreateAccountDialog
from School_System.windows.ForgotPasswordDialog import ForgotPasswordDialog
from School_System.windows.AddRemoveDB import AddRemoveDB

from School_System.windows.IndexSU import IndexSU
import School_System.helpers.db_utils as database
import School_System.helpers.settings as settings
import School_System.resources.qrc.rec_rc




class Login(QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi(LOGIN, self)

        self.setWindowTitle("Login")
        self.login_button.clicked.connect(self.authenticate_user)
        self.create_account_button.clicked.connect(self.open_create_account_dialog)
        self.forget_password_button.clicked.connect(self.forget_password)
        self.add_db_button.clicked.connect(self.open_add_remove_db_dialog)
        #aself.view_password_button.clicked.connect(self.toggle_password_visibility)
        self.remember_me_button.toggled.connect(self.remember_me)
        self.apply_floating_effect(self.widget)
        #self.widget.setStyleSheet("background-color: white;")
        #self.setAutoFillBackground(True)
        self.db_manager = db_manager_instance

        self.active_db = None

        self.load_settings()
        self.start_up_script()










    def remember_me(self, checked):
        if checked:
            settings.set_remember_true()

        else:
            settings.set_remember_false()






    def forget_password(self):
        self.open_forget_password_dialog()




    def open_create_account_dialog(self):
        # Create an instance of the CreateAccountDialog
        create_account_dialog = CreateAccountDialog(self)  
        create_account_dialog.exec()



    def open_forget_password_dialog(self):
        forget_password_dialog = ForgotPasswordDialog(self)
        forget_password_dialog.exec()

    def open_add_remove_db_dialog(self):
        add_remove_db_dialog = AddRemoveDB(self)
        add_remove_db_dialog.finished.connect(self.start_up_script)
        add_remove_db_dialog.exec()



    def toggle_password_visibility(self):
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)





    def start_up_script(self):
        db_list = self.db_manager.get_all_databases()

        if not db_list:
            self.db_indicator.setText("Create a Database")
            self.active_db = False


        elif not any("(current)" in db for db in db_list):
            self.db_indicator.setText("Select a Database")
            self.active_db = False


        else:
            current_db = next(db for db in db_list if "(current)" in db)
            current_db_name = current_db.replace(" (current)", "")
            self.db_indicator.setText(current_db_name)
            self.active_db = True


    def authenticate_user(self):

        if not self.active_db:
            print("ss")
            return

        email = self.email_field.text()
        password = self.password_field.text()

        # Validate inputs
        if not email or not password:
            QMessageBox.warning(self, "Input Error", "Both email and password fields must be filled.")
            return
        
        evaluate = database.login_user(email,password)

        if evaluate == database.SUPERADMIN:
            QMessageBox.information(self, "superadmin",f"Welcome {database.LOGGED_IN_USER_NAME}")
            self.remember_mail(email)
            self.index_window = IndexSU()
            self.index_window.show()   
            self.close()    



        elif evaluate == database.ADMIN:
            QMessageBox.information(self, " admin",f"Welcome {database.LOGGED_IN_USER_NAME}")
            # Load the IndexSU window(for admins)
            self.remember_mail(email)
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



    def load_settings(self):
        if settings.remember_mail():
            if settings.remember_mail() == " ":
                self.remember_me_button.setChecked(True)
                return
            self.email_field.setText(settings.remember_mail())
            self.remember_me_button.setChecked(True)




    def remember_mail(self,email):
        if settings.remember_mail():
            settings.add_email(email)




