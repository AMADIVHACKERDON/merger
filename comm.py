import smtplib
import ssl
from email.message import EmailMessage

subject = 'email with python'
body  = 'this is a test email from python'
sender_email = 'victory.amadi@stu.cu.edu.ng'
receiver_email = 'victory.amadi@stu.cu.edu.ng'
password = input('enter password:')

message = EmailMessage()
message['FROM'] = sender_email
message['to'] = receiver_email
message['subject'] = subject


html = f"""
   <html>
      <body>
         <h1>{subject}</h1>
         <p>{body}</p>
      </body>
   </html>
"""
message.add_alternative(html, subtype = 'html')

context = ssl.create_default_context()
print('sending email')
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email,receiver_email,message.as_string())
print('success')