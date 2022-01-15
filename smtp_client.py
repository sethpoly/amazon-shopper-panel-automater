import smtplib

from mail import Mail

class SmtpClient():
    host = "smtp.gmail.com"
    port = 587
    mailServer = smtplib.SMTP(host=host, port=port)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def open_connection(self):
        """
        Open a connection with SMTP mail server

        Parameters
        ----------
        user: str
            gmail username
        password: str
            gmail password (application specific one)
        """
        # identify ourselves to smtp mail client
        self.mailServer.ehlo()  
        # secure email connection
        self.mailServer.starttls()
        # re-identify as secure connection
        self.mailServer.ehlo()
        # login
        self.mailServer.login(user=self.username, password=self.password)

    def close_connection(self):
        """Close connection with SMTP mail server"""
        self.mailServer.quit()

    def send_mail(self, mail:Mail):
        from_addr = mail.msg["From"]
        to_addr = mail.msg["To"]
        message = mail.msg

        self.mailServer.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=message.as_string())
        print(f'-------------\nForwarding email:\n{mail}------------------')


    
