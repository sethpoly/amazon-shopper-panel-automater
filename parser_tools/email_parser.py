from bs4 import BeautifulSoup
import re

class EmailParser():

    # Clean email output of all script tags/html/css etc
    @classmethod
    def clean_text(cls, text):
        text = re.sub(r'\. \{.*\}', '', text)  # Strip CSS
        text = EmailParser.remove_whitespace(text)  # Remove invisible carriage returns etc

        soup = BeautifulSoup(text, 'html.parser')
        for s in soup(['script', 'style']):
            s.extract()
        return ' '.join(soup.stripped_strings)


    # Remove all white space and carriage returns
    @classmethod
    def remove_whitespace(cls, text):
        chars = ['\n', '\t', '\r']
        for ch in chars:
            if ch in text:
                text = text.replace(ch, '')
        return text