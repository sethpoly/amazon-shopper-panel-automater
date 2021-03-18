# Loop through all emails starting from most recent
# Using receipt classifier, determine if is valid receipt
# Send email to amazon shopper panel email adress if valid
# Continue until 15 successful emails sent
def check_mail():
    print('Checking mail for receipts...')