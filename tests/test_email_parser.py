import unittest
from parser_tools.email_parser import EmailParser


class TestEmailParser(unittest.TestCase):
    def test_remove_newline(self):
        # we successfully remove all white spave
        text = "Hello\n World\n\n\n"
        cleanedText = EmailParser.clean_text(text)
        self.assertEqual(cleanedText, "Hello World")

if __name__ == '__main__':
    unittest.main()