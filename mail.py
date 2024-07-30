import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from dotenv import load_dotenv
from email import encoders

# Load all environment variables
load_dotenv()


HOST= os.getenv('HOST')
PORT = os.getenv('PORT')
PASSWORD = os.getenv('PASSWORD')
SENDER = os.getenv('SENDER')
RECIEVER = os.getenv('RECIEVER')

# Create an email message object.
# Using alternative gives us options to send email message either a plain or 
# HTML version of our email message depending on the 
# One that suits our email client
message = MIMEMultipart('alternative')
message['Subject'] = 'Python Mail Testing'
message['From'] = SENDER
message['To'] = RECIEVER

# Creating a plain message
text = '''\
    This is a plain text version of our mail
    
    Welcome to my python send mail test
    I'm excited to tell you that it worked
    '''
    
# Reading html file
html = ''
with open('mail.html', 'rt') as file:
    html = file.read()
    
html_obj = MIMEText(html, 'html')
text_obj = MIMEText(text, 'plain')

# Reading attatchment and attach 
file_name = 'students.pdf'

with open(file_name, 'rb') as file:
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(file.read())
    
# Encode file in ASCII characters to send by email    
encoders.encode_base64(attachment)
      
# Add header as key/value pair to attachment part
attachment.add_header("Content-Disposition",f"attachment;filename= {file_name}",
        )
    
# Attaching file to email object
message.attach(attachment)

# Attatching both plain and html versions of our message to the email object
message.attach(text_obj)
message.attach(html_obj)

# Create a secured connection
try:
    context = ssl.create_default_context()

    # # Connect to smtp server
    with smtplib.SMTP_SSL(host=HOST, context=context, port=PORT) as server:
        server.login(user=SENDER, password=PASSWORD)
        server.sendmail(SENDER, RECIEVER, message.as_string())
        print('Mail Sent')
        
except Exception as err:
    print(f'An error ocurred: {err}')