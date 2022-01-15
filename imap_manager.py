import imaplib
import time
import traceback

class ImapManager():
    """manages authentication, logout, and overall imap session"""

    def __init__(self, username, password):
        self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
        self.username = username
        self.password = password
        self.open_connection()

    def open_connection(self):
        """Authenticate a imap session instance using class level credentials"""
        try:
            (retcode, capabilities) = self.imap.login(self.username, self.password)
            print(f'Logged in as {self.username} at {time.strftime("%H:%M:%S", time.localtime())}.')
        except imaplib.IMAP4.error:
            traceback.print_exc()


    def close_connection(self):
        """Close the imap connection"""
        
        try:
            self.imap.close()
            self.imap.logout()
            print('Closed the connection.')
        except imaplib.IMAP4.error:
            print('Error: Connection failed to close.')