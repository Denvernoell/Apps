
# from my_secrets import username, app_password
import smtplib
from email.message import EmailMessage


def email_alert(to, subject, body, email='personal'):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['to'] = to

    # From denvernoell@gmail.com
    if email == 'personal':

        msg['from'] = username
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

    # From apps@denvernoell.com
    elif email == 'apps':
        msg['from'] = 'apps@denvernoell.com'
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    server.login(username, app_password)
    server.send_message(msg)
    server.quit()
