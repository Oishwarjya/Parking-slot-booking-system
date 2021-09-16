#Imports
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib,ssl
import random
import time
import os

from Mainapp import Entry

#Import for secure variables which are then pushed into os.environ
from dotenv import load_dotenv
load_dotenv()

def send_reset_pwd_mail(email : str):
    backemail_add = os.environ.get('BACKEND_MAIL_ADDR')
    backemail_pwd = os.environ.get('BACKEND_MAIL_PWD')
    #backemail_add = os.getenv('BACKEND_MAIL_ADDR')
    #backemail_pwd = os.getenv('BACKEND_MAIL_PWD')
    
    #Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd) 

    verif_code = Entry.add_verif_code(email,0)

    url = "http://localhost:8000/reset_pwd"                 

    #User mail subject, body and format of the mail
    subject = 'Parking Slot Booking System: Reset Your Password'
    body = f'Dear User \n\nPlease Click on the Link Below to Reset your Parking Slot Booking website Password for your {email} account. \n\nThis is your 6 Digit Verification Code: {verif_code} \n\nReset Link: {url} \n\nIf you DID NOT ask to reset your password please IGNORE this email!\n\nThank you! \n\nWarm Regards, \n\nThe Help Team \nPropertyManagerApp'
    msg = f'Subject: {subject}\n\n{body}'

    #Sends the mail with the data and quits the server
    server.sendmail(backemail_add,email,msg)
    print("MAIL SENT SUCCESSFULLY")
    server.quit()

def send_mail_with_attachment(filename : str, attachment : str, email : str):
    backemail_add = os.environ.get('BACKEND_MAIL_ADDR')
    backemail_pwd = os.environ.get('BACKEND_MAIL_PWD')

    #Creates the mail object
    msg = MIMEMultipart()
    msg['From'] = backemail_add
    msg['To'] = email
    
    #Builds the mail
    msg['Subject'] = "#:"
    body = "Dear User\n\nPlease find attached ...\n\nThank you!\n\nWarm Regards,\n\nPropertyManagerApp"
    msg.attach(MIMEText(body, 'plain'))
    
    #File to be attached
    filename = filename
    attachment = open(attachment, "rb")

    #Attachment is encoded and attached to the mail
    att = MIMEBase('application', 'octet-stream')
    att.set_payload((attachment).read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(att)
    
    #Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)       

    #Message is converted to a string and sent
    text = msg.as_string()
    server.sendmail(backemail_add, email, text)
    print("MAIL SENT SUCCESSFULLY")
    server.quit()

def send_feedback_mail(email : str, name : str, message : str):
    backemail_add = os.environ.get('BACKEND_MAIL_ADDR')
    backemail_pwd = os.environ.get('BACKEND_MAIL_PWD')
    #backemail_add = os.getenv('BACKEND_MAIL_ADDR')
    #backemail_pwd = os.getenv('BACKEND_MAIL_PWD')
    
    #Starts a server on port 465 and logs into senders email id so it can send the mail
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login(backemail_add,backemail_pwd)            

    #User mail subject, body and format of the mail - FROM ADMIN TO USER
    subject1 = 'Parking Slot Booking System: Query/Feedback Received'
    body1 = f'Dear {name} \n\nThank you for reaching out to us! \n\nYour Query/Feedback has been received successfully! \n\nPlease wait until we process the information and get back to you. \n\nHope you have a wonderful day! \n\nWarm Regards, \n\nThe Help Team \nPropertyManagerApp'
    msg1 = f'Subject: {subject1}\n\n{body1}'

    #User mail subject, body and format of the mail - FROM WEBSITE TO ADMIN
    subject2 = 'Parking Slot Booking System: Query/Feedback Generated'
    body2 = f'Dear Admin \n\n{name} has generated the following query/feedback \n\nQUERY/FEEDBACK: {message}\n\nPlease get in touch with the user and respond accordingly\n\nThank you! \n\nWarm Regards, \n\nThe Help Team \nPropertyManagerApp'
    msg2 = f'Subject: {subject2}\n\n{body2}'

    #Sends the mail with the data and quits the server
    server.sendmail(backemail_add,email,msg1)
    server.sendmail(email,backemail_add,msg2)
    print("MAIL SENT SUCCESSFULLY")
    server.quit()

if __name__=='__main__':
    #send_mail("ohitsmeoishee@gmail.com")
    #send_mail_with_attachment("ohitsmeoishee@gmail.com")
    pass