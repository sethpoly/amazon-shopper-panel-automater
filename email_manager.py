from email.message import Message
from mail import Mail
from parser_tools.email_parser import EmailParser
import email

class EmailManager:
    """manages the incoming emails, makes a prediction, and delegates organization cleanup"""
    mails = []

    def __init__(self, categories, classifier, imapManager):
        self.categories = categories
        self.classifier = classifier
        self.imapManager = imapManager

    # Loop through all emails starting from most recent
    # Using receipt classifier, determine if is valid receipt
    # Send email to amazon shopper panel email address if valid
    # Continue until X successful emails are sent
    def check_mail(self):
        emailsToCheck = 10
        count = 0
        print(
            f"Checking mail for receipts for the next {emailsToCheck} emails..")

        status, messages = self.imapManager.imap.select("INBOX")
        if status != "OK":
            exit("Incorrect mail box")

        for i in range(int(messages[0]), 1, -1):
            if not count <= emailsToCheck:
                return
            count += 1

            res, msg = self.imapManager.imap.fetch(str(i), "(RFC822)")
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

        self.imapManager.close_connection()

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

    # If determined as receipt, forward email to amazon {use correct 'from' address}
    def __forward_email(email):
        print('Forwarding email to receipts@panel.amazon.com...')
