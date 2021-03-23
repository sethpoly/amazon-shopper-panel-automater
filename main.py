import service_account as acc
import gspread
import imaplib
import os
import time
import traceback


# gmail account credentials
username = os.environ['GMAIL_RECEIPTS']
password = os.environ['GMAIL_RECEIPTS_PASS']

# create IMAP4 class with SSL
imap = imaplib.IMAP4_SSL('imap.gmail.com')

# authenticate (if fails: <allow less secure apps in gmail account>)
def authenticate():
    try:
        (retcode, capabilities) = imap.login(username, password)
        print(f'Logged in as {username} at {time.strftime("%H:%M:%S", time.localtime())}.')
    except imaplib.IMAP4.error:
        traceback.print_exc()

# Close the imap connection
def close_connection():
    try:
        imap.close()
        imap.logout()
        print('Closed the connection.')
    except imaplib.IMAP4.error:
        print('Error: Connection failed to close.')


# Loop through all emails starting from most recent
# Using receipt classifier, determine if is valid receipt
# Send email to amazon shopper panel email address if valid
# Continue until 15 successful emails sent
def check_mail():
    print('Checking mail for receipts...')


# If determined as receipt, forward email to amazon {use correct 'from' address}
def forward_email():
    print('Forwarding email to receipts@panel.amazon.com...')


spreadsheet = acc.Spreadsheet('AmazonReceipts', 'Sheet1').sheet
authenticate()
