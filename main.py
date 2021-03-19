# Loop through all emails starting from most recent
# Using receipt classifier, determine if is valid receipt
# Send email to amazon shopper panel email address if valid
# Continue until 15 successful emails sent
def check_mail():
    print('Checking mail for receipts...')


# If determined as receipt, forward email to amazon {use correct 'from' address}
def forward_email():
    print('Forwarding email to receipts@panel.amazon.com...')