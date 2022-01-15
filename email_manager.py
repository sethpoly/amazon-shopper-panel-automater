from email.message import Message
from re import I
from classifier import Classifier
from imap_client import ImapClient
from mail import Mail
from parser_tools.email_parser import EmailParser
import email
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from smtp_client import SmtpClient
import os
import time

class EmailManager:
    """manages the incoming emails, makes a prediction, and delegates organization cleanup"""
    mails = []

    def __init__(self, categories, classifier:Classifier, imap_client:ImapClient):
        self.categories = categories
        self.classifier = classifier
        self.imap_client = imap_client

    # Loop through all emails starting from most recent
    # Using receipt classifier, determine if is valid receipt
    # Send email to amazon shopper panel email address if valid
    # Continue until X successful emails are sent
    def check_mail_and_forward(self, emails_to_forward:int, forward_category:str, recipient:str):
        # open smtp connection
        self.smtp = SmtpClient(username=os.environ['SMTP_EMAIL'], password=os.environ['SMTP_PASSWORD'])
        self.smtp.open_connection()

        emails_to_check = 100
        checked_emails_count = 0
        forwarded_emails_count = 0
        print(
            f"Checking mail for receipts for the next {emails_to_check} emails..")

        status, messages = self.imap_client.imap.select("INBOX")
        if status != "OK":
            exit("Incorrect mail box")

        for i in range(int(messages[0]), 1, -1):
            # guard haven't reached check limit
            if not checked_emails_count <= emails_to_check:
                return

            # guard haven't reached the forward limit yet
            if not forwarded_emails_count <= emails_to_forward:
                return

            checked_emails_count += 1
            res, msg = self.imap_client.imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    body = EmailParser.clean_text(self.__getBodyFromMessage(msg=msg))

                    # Predict mail category 
                    prediction = self.classifier.predict(
                        body, self.categories[0], self.categories[1])

                    # build mail object
                    mail = Mail(msg=msg, category=prediction, body=body)
                    print(str(mail))

                    # testing
                    if mail.category == forward_category:
                        self.__forward_email(mail=mail, recipient=recipient)
                        forwarded_emails_count += 1
                    
                    self.__store_in_inbox(mail=mail,index=str(i))

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

        self.smtp.close_connection()
        self.imap_client.close_connection()

    def __getBodyFromMessage(self, msg: Message):
        """get body from a message object
            Parameters
            ----------
            msg: Message
        """

        body = ""
        # Grab the body of the email
        for part in msg.walk():
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
        return body

    def __forward_email(self, mail, recipient):
        """
        Forward email to specicied recipient

        Parameters
        ----------
        mail:Mail
            the email to forward
        recipient:str
            the client to receive the email
        """
        # delay so recipient doesn't blacklist you lol
        time.sleep(1.5)

        # mutate email until a forwardable email
        email_to_forward = self.__generate_forward_email(mail=mail, recipient=recipient)

        # forward!
        self.smtp.send_mail(mail=email_to_forward)

    def __generate_forward_email(self, mail:Mail, recipient:str) -> Mail:
        """
        Generate an email to forward using an existing email

        Parameters
        ----------
        mail:Mail
            the existing email to change the headers of
        recipient:str
            the client to forward the email to
        """
        # replace headers
        msg = MIMEMultipart()
        msg['From'] = self.smtp.username
        msg['To'] = recipient
        msg['Subject'] = mail.subject
        body = mail.body
        msg.attach(MIMEText(body))

        return Mail(msg, category=mail.category, body=body)

    def __store_in_inbox(self, mail: Mail, index):
        self.imap_client.imap.store(index, '+X-GM-LABELS', f'{mail.category}')
        self.imap_client.imap.store(index, '+X-GM-LABELS', '"CheckedButPrimary"')

        # Remove SEEN flag
        self.imap_client.imap.store(index, '-FLAGS', '\\Seen')

         # Delete from primary inbox
        self.imap_client.imap.store(index, '+FLAGS', '\\Deleted')

