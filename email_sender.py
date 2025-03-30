import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_with_attachment(subject, body, from_email, to_email, file_paths):
    # Mailtrap SMTP credentials
    smtp_host = "smtp.mailtrap.io"  # Replace with your Mailtrap SMTP host
    smtp_port = 587                 # Common ports: 25, 2525, 587
    smtp_username = "15fec4d7e2f9c5" # Replace with your Mailtrap username
    smtp_password = "abd8d2d73ca664" # Replace with your Mailtrap password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

   
    for file_path in file_paths:
        if os.path.exists(file_path):
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)
        else:
            print(f"File not found: {file_path}")
            return

    # Send the email via Mailtrap's SMTP server
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            print("Email with attachment sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")