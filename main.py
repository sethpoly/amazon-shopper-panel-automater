from email_manager import EmailManager
from parser_tools.email_parser import EmailParser
from classifier import Classifier
from imap_client import ImapClient
from spreadsheet import Spreadsheet
import email
import os
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()  

spreadsheet = Spreadsheet(sheet_name='AmazonReceipts', sheet_page='Sheet1')
classifier = Classifier(spreadsheet=spreadsheet)
imap_client = ImapClient(os.environ['IMAP_EMAIL'], os.environ['IMAP_PASSWORD'])
categories = ("receipt", "not_receipt")

# recipient to forward emails to
recipient = "receipts@panel.amazon.com"

# manages the classifying, sorting, parsing of emails
email_manager = EmailManager(categories=categories, classifier=classifier, imap_client=imap_client)
email_manager.check_mail_and_forward(emails_to_forward=15, forward_category=categories[0], recipient=recipient)
