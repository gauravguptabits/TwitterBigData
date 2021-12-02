
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(sender_email,sender_email_password,e):
  # sender_email = ""
  # sender_email_password = ""
  receiver_email = ["harsh2013@gmail.com", "harsh.vardhan@impressico.com"]
  message = MIMEMultipart("alternative")
  message["Subject"] = "Big Data POC Notification"
  message["From"] = sender_email
  message["To"] =  ", ".join(receiver_email)

  # Create the plain-text and HTML version of your message
  text = """\
  Hi Team,
  This is to notify you that Twitter Streming has stoped working.
  Please loging to server to restart it manually.
  Regards
  BigData POC Team"""
  html = """\
  <html>
    <body>
      <p>Hi Team,<br>
        This is to notify you that Twitter Streming has stoped working. 
        <br>Please logging to server to restart it manually.
        <br>Error Type: %s
        <br>Error Doc: %s
        <br>Error :%s
        <br>Regards
        <br>BigData POC Team
      </p>
    </body>
  </html>
  """%(e.__class__.__name__,e.__doc__, e) 

  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, sender_email_password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )

  return "Mail sent successfully"


