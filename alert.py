import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# plkxccgafzjmtwtp - two factor password
# Your Gmail account settings
sender_email = "edreminder0@gmail.com"  # Replace with your Gmail address
sender_password = 'plkxccgafzjmtwtp'  # app specific password
# "ElE1234_!@#67890" d

# Recipient's email address
recipient_email = "eli.smitty04@gmail.com"  # Replace with the recipient's email address

# Compose the email
subject = "Take ED Sample"
body = "Hey, this is a reminder to take your sample!"

# Create a message container
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Connect to the Gmail SMTP server
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    print("Email sent successfully.")
except Exception as e:
    print("An error occurred:", e)
