from email import message
from email_parser import EmailParser
from classifier import Classifier
from spreadsheet import Spreadsheet
import email
import imaplib
import os
import time
import traceback
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# setup ML model
classifier = Classifier()
classifier.clean_data()
classifier.fit()

# gmail account credentials
username = os.environ['GMAIL_EMAIL']
password = os.environ['GMAIL_PASSWORD']

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
    emailsToCheck = 10
    count = 0
    print(f'Checking mail for receipts for the next {emailsToCheck} emails..')

    status, messages = imap.select('INBOX')
    if status != 'OK': exit('Incorrect mail box')

    for i in range(int(messages[0]), 1, -1):
        if not count <= emailsToCheck:
            return
        count += 1

        res, msg = imap.fetch(str(i), '(RFC822)')
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                sender = msg['From']
                subject = msg['Subject']
                print(sender)
                print(subject)

                # Grab the body of the email
                for part in msg.walk():
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                body = EmailParser.clean_text(body)  # Clean formatting of email
                print(body)

                # Predict if the email is a receipt
                prediction = classifier.predict(body)
                print(prediction)
                # if prediction == 'reject':  # move to reject inbox
                #     typ, /data = imap.store(num, '+X-GM-LABELS', '"Application Updates"')
                #     add_reject_row(company_name, body)  # Add entry to spreadsheet

                # Remove SEEN flag
                # typ, data = imap.store(num, '-FLAGS', '\\Seen')
                # # Move to CHECKED inbox
                # typ, data = imap.store(num, '+X-GM-LABELS',
                #                        'Checked')
                # # Delete from inbox
                # typ, data = imap.store(num, '+FLAGS', '\\Deleted')

    close_connection()


# If determined as receipt, forward email to amazon {use correct 'from' address}
def forward_email(email):
    print('Forwarding email to receipts@panel.amazon.com...')


spreadsheet = Spreadsheet('AmazonReceipts', 'Sheet1').sheet
authenticate()
check_mail()
