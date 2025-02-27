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

load_dotenv()




class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(FORGET_PASSWORD_DIALOG, self)

        self.setWindowTitle("forget password")

        self.check_mail_button.clicked.connect(self.check_email)
        self.user_mail = None
        self.reset_code = None







    def check_email(self):
        email = self.email_field.text()

        if not email:
            return


        if database.email_exists(email):
            self.frame.hide()
            self.user_mail = email
            self.send_reset_email()
            return


        self.warnning.setText("email does not esist")







    def send_reset_code(self):
        self.reset_code = str(random.randint(100000, 999999))  # Generate a 6-digit code


        # Email setup (Use your email & app password)
        sender_email = "your-email@gmail.com"
        sender_password = "your-app-password"  # Use an app password, not your real password!

        message = f"Subject: Password Reset Code\n\nYour reset code is: {self.reset_code}"

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, self.user_mail, message)
            return True  # Email sent successfully
        except Exception as e:
            print("Error sending email:", e)
            return False




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