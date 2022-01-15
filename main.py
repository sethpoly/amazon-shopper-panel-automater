from email_manager import EmailManager
from parser_tools.email_parser import EmailParser
from classifier import Classifier
from imap_manager import ImapManager
from spreadsheet import Spreadsheet
import email
import os
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()  

spreadsheet = Spreadsheet(sheet_name='AmazonReceipts', sheet_page='Sheet1')
classifier = Classifier(spreadsheet=spreadsheet)
imapManager = ImapManager(os.environ['GMAIL_EMAIL'], os.environ['GMAIL_PASSWORD'])
categories = ("receipt", "not_receipt")

# manages the classifying, sorting, parsing of emails
emailManager = EmailManager(categories=categories, classifier=classifier, imapManager=imapManager)
emailManager.check_mail()
