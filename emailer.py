import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart   # ✅ Added import
import logging

def send_email(subject, body):
    sender = "nanduripranathi57@gmail.com"       # Replace with your Gmail
    receiver = "22r11a6729@gcet.edu.in"     # Replace with recipient
    password = "gdet ylgu ukwy vyfc"   # Replace with App Password

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)   # ✅ Works with Gmail app password
            server.sendmail(sender, receiver, msg.as_string())

        logging.info(f"✅ Email sent successfully to {receiver} with subject: {subject}")
        print(f"✅ Email sent successfully to {receiver} with subject: {subject}")

    except Exception as e:
        logging.error(f"❌ Failed to send email: {str(e)}")
        print(f"❌ Failed to send email: {str(e)}")
