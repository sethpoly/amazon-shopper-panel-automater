from email.message import Message

class Mail():
    category = ""

    def __init__(self, msg:Message, category, body):
        self.msg = msg
        self.sender = msg["From"] 
        self.subject = msg["Subject"]
        self.dateReceived = msg["Date"]
        self.body = body
        self.category = category

    def __str__(self):
        return f'From: {self.msg["From"]}\nTo: {self.msg["To"]}\nSubject:{self.subject}\nDate Received:{self.dateReceived}\nBody: {self.body}\nCategory: {self.category}\n'