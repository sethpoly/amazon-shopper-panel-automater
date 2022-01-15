import imaplib
import time
import traceback

class ImapManager():
    def __init__(self, username, password):
        self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
        self.username = username
        self.password = password
        self.__authenticate()

    # Authenticate a imap session instance using class level credentials
    def __authenticate(self):
        try:
            (retcode, capabilities) = self.imap.login(self.username, self.password)
            print(f'Logged in as {self.username} at {time.strftime("%H:%M:%S", time.localtime())}.')
        except imaplib.IMAP4.error:
            traceback.print_exc()


    # Close the imap connection
    def close_connection(self):
        try:
            self.imap.close()
            self.imap.logout()
            print('Closed the connection.')
        except imaplib.IMAP4.error:
            print('Error: Connection failed to close.')