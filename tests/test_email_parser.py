import unittest
from parser_tools.email_parser import EmailParser


class TestEmailParser(unittest.TestCase):
    def test_remove_whitespace(self):
        # we successfully remove all white spave
        text = "Hello\n World\n\n\n\t\r"
        cleanedText = EmailParser.remove_whitespace(text)
        self.assertEqual(cleanedText, "Hello World")

    def test_clean_text(self):
        # remove all html elements & tags from text
        text = "<h1>Header.</h2><p>This is a paragraph.</p>"
        cleanedText = EmailParser.clean_text(text)
        self.assertEqual(cleanedText, "Header. This is a paragraph.")

if __name__ == '__main__':
    unittest.main()