import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class EmailSender:
    def __init__(self):
        self.login = '213351@edu.p.lodz.pl'
        self.mail = '213351@p.lodz.pl'
        self.server = smtplib.SMTP('smtp.p.lodz.pl:587')

    def connect(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.login, 'fuZa!ud%ida')

    def send_mail(self, target_mail, message):
        msg = MIMEMultipart()
        msg['Subject'] = 'Open Ticket'
        msg['From'] = self.mail
        msg['To'] = target_mail
        final_message = 'Your ticket has been generated. Its content is given here: \n\n' + message
        msg.attach(MIMEText(final_message, 'plain'))

        self.server.sendmail(self.mail, target_mail, msg.as_string())