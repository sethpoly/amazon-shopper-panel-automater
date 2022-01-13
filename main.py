from parser_tools.email_parser import EmailParser
from classifier import Classifier
from imap_manager import ImapManager
from spreadsheet import Spreadsheet
import email
import os
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()  

# setup ML model
classifier = Classifier(sheet_name='AmazonReceipts', sheet_page='Sheet1')

# setup imap session
imapManager = ImapManager(os.environ['GMAIL_EMAIL'], os.environ['GMAIL_PASSWORD'])

# Loop through all emails starting from most recent
# Using receipt classifier, determine if is valid receipt
# Send email to amazon shopper panel email address if valid
# Continue until X successful emails are sent
def check_mail():
    emailsToCheck = 10
    count = 0
    print(f'Checking mail for receipts for the next {emailsToCheck} emails..')

    status, messages = imapManager.imap.select('INBOX')
    if status != 'OK': exit('Incorrect mail box')

    for i in range(int(messages[0]), 1, -1):
        if not count <= emailsToCheck:
            return
        count += 1

        res, msg = imapManager.imap.fetch(str(i), '(RFC822)')
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
                prediction = classifier.predict(body, 'receipt', 'not_receipt')
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

    imapManager.close_connection()


# If determined as receipt, forward email to amazon {use correct 'from' address}
def forward_email(email):
    print('Forwarding email to receipts@panel.amazon.com...')


spreadsheet = Spreadsheet('AmazonReceipts', 'Sheet1').sheet
imapManager.authenticate()
check_mail()
