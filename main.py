import service_account as acc
import gspread
import email
import imaplib
import os
import time
import traceback
from bs4 import BeautifulSoup
import re

# gmail account credentials
username = os.environ['GMAIL_RECEIPTS']
password = os.environ['GMAIL_RECEIPTS_PASS']

# create IMAP4 class with SSL
imap = imaplib.IMAP4_SSL('imap.gmail.com')


# Clean email output of all script tags/html/css etc
def clean_text(text):
    text = re.sub(r'\. \{.*\}', '', text)  # Strip CSS
    text = remove_whitespace(text)  # Remove invisible carriage returns etc

    soup = BeautifulSoup(text, 'html.parser')
    for s in soup(['script', 'style']):
        s.extract()
    return ' '.join(soup.stripped_strings)


# Remove all white space and carriage returns
def remove_whitespace(text):
    chars = ['\n', '\t', '\r']
    for ch in chars:
        if ch in text:
            text = text.replace(ch, '')
    return text


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

# TODO: Filter emails by ORDER RECEIVED keywords
def check_mail():
    print('Checking mail for receipts...')
    # Connect to mailbox
    #status, messages = imap.select('INBOX')
    imap.select('INBOX')
    status, messages = imap.search(None, '(SUBJECT "order # confirmed") (BODY "Order confirmed")')
    n = 5  # Emails to parse

    temp_string = str(messages[0])
    temp_arr = temp_string.split(' ')
    print(temp_arr[1])

    messages = int(temp_arr[1])
    if status == 'OK':
        for i in range(messages, messages - n, -1):  # Reverse traversal
            print('Processing email: ')
            body = ''
            typ, data = imap.fetch(str(i), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    original = email.message_from_bytes(response_part[1])

                    company_name = original['From']
                    print(company_name)
                    print(original['Subject'])

                    # Grab the body of the email
                    for part in original.walk():
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                    body = clean_text(body)  # Clean formatting of email
                    print(body)

                    # Predict if the email is a rejection email
                    # prediction = classifier.predict(body)
                    # print(prediction)
                    # if prediction == 'reject':  # move to reject inbox
                    #     typ, data = imap.store(num, '+X-GM-LABELS', '"Application Updates"')
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
def forward_email():
    print('Forwarding email to receipts@panel.amazon.com...')


spreadsheet = acc.Spreadsheet('AmazonReceipts', 'Sheet1').sheet
authenticate()
check_mail()
