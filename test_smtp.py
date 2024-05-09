import smtplib
from email.mime.text import MIMEText

# SMTP server details
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Email credentials
sender_email = 'libraryb78@gmail.com'
sender_password = 'Library-78book'

# Create a secure connection to the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()

# Login to the SMTP server
server.login(sender_email, sender_password)

# Close the connection
server.quit()
