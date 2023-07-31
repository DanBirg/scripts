import smtplib
from email.mime.text import MIMEText

# Set up the email message
msg = MIMEText("You are doing a great job!"
               "your friend - the snake")

msg['From'] = 'somesnake@somemail.com'
msg['To'] = 'kobra@somemail.com'
msg['Subject'] = 'snakes on the plane'

# Setting up the SMTP server
smtp_server = 'mailserver.somemail.com'
smtp_port = 25  # or 465 for SSL

# Creating the SMTP object
smtp_obj = smtplib.SMTP(smtp_server, smtp_port)

# Sending the email
smtp_obj.sendmail(msg['From'], [msg['To']], msg.as_string())

# Closing the SMTP connection
smtp_obj.quit()

