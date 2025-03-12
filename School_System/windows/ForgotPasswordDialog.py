import os
from dotenv import load_dotenv

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
import School_System.helpers.db_utils as database
from School_System.ui import FORGET_PASSWORD_DIALOG
import smtplib
import random
from email.message import EmailMessage
import bcrypt
from PyQt6.QtCore import  Qt
from PyQt6.QtCore import QTimer

load_dotenv()




class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(FORGET_PASSWORD_DIALOG, self)

        self.setWindowTitle("forget password")

        self.check_mail_button.clicked.connect(self.check_email)
        self.user_mail = None
        self.reset_code = None

        self.check_code.clicked.connect(self.verify_code)
        self.change_pass_button.clicked.connect(self.change_password)


        self.warnning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)



    def check_email(self):
        email = self.email_field.text()

        if not email:
            return


        if database.email_exists(email):
            self.user_mail = email
            check = self.send_reset_email()
            if check:
                self.frame.hide()
                return

            self.warnning.setText("check your internet connection or try later")
            return


        self.warnning.setText("email does not exist")
        QTimer.singleShot(2000, self.warnning.clear)



    def verify_code(self):
        code = self.code_filed.text()

        if not code: return


        if code == self.reset_code:
            self.frame_2.hide()
            return


        self.label_2.setText("wrong code")
        QTimer.singleShot(2000, self.label_2.clear)





    def change_password(self):
        pass1 = self.pass_1.text()
        pass2 = self.pass_2.text()

        if not pass1 : return

        if pass1 != pass2:
            self.label_5.setText("password do not match")
            QTimer.singleShot(2000, self.label_5.clear)
            return


        hash_password = self.hash_password(pass1)

        ### database update password where email = ?




    def send_reset_email(self):
        self.reset_code = str(random.randint(100000, 999999))

        SMTP_SERVER = os.environ.get("SMTP_SERVER")
        SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
        GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
        GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

        msg = EmailMessage()
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = self.user_mail
        msg["Subject"] = "Password Reset Code"
        msg.set_content(f"Your reset code is: {self.reset_code}")

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
                server.send_message(msg)

            print("✅ Reset email sent successfully!")
            return True
        except Exception as e:
            print("❌ Error sending email:", e)
            return False





    def hash_password(self,password: str) -> str:
        # Generate a salt
        salt = bcrypt.gensalt()
        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')