import smtplib
from email.mime.text import MIMEText
from email.header import Header


class NotificationSendingFailed(Exception):
    pass


class MailSender:
    server = smtplib.SMTP('smtp.gmail.com:587')

    def send_email(self, sender, receiver, password, subject, body):
        try:
            self.server.starttls()
            self.server.ehlo()
            self.server.login(sender, password)
            coding = 'utf-8'
            msg = MIMEText(body, 'plain', coding)
            msg['Subject'] = Header(subject, coding)
            self.server.sendmail(sender, receiver, msg.as_string())
            self.server.quit()
        except smtplib.SMTPAuthenticationError:
            raise NotificationSendingFailed("Wrong credentials")
