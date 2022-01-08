import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from service_account import Spreadsheet

# Handles the data for receipt classifier
# Uses sklearn, pandas, and Naive Bayes to predict if an email is a receipt or not
class Classifier:
    def __init__(self):
        self.df = self.get_csv()
        self.x_train, self.x_test, self.y_train, self.y_test = None, None, None, None
        self.nb = MultinomialNB()
        self.vectorizer = CountVectorizer()
        self.encoder = LabelEncoder()

    # Retrieve most recent receipt data set from sheets API
    def get_csv(self):
        data_sheet = Spreadsheet('AmazonReceipts', 'Sheet1').sheet
        rows = data_sheet.get_all_values()
        return pd.DataFrame.from_records(rows)

        # Removes punctuation, HTML, from EMAIL column in data set
        # df[0] is EMAIL, df[1] is STATUS

    def clean_data(self):
        try:
            self.df[0] = self.df[0].apply(lambda x: x.lower())
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', '\n')))
            print('Successfully cleaned data.')
        except AttributeError as e:
            print(f'Whoops: {repr(e)}')

        # Fit data using Naive Bayes classifier

    def fit(self):
        # pull data into vectors to create collection of text/tokens

        x = self.vectorizer.fit_transform(self.df[0])
        y = self.encoder.fit_transform(self.df[1])

        # split into train and test sets
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2)

        # Fit dataset in naive bayes classifier
        self.nb.fit(self.x_train, self.y_train)

    # Predict if @param email is rejection or not
    def predict(self, email):
        category_names = {'receipt': 'receipt', 'not_receipt': 'not_receipt'}
        cod = self.nb.predict(self.vectorizer.transform([email]))
        return category_names[self.encoder.inverse_transform(cod)[0]]

    def print_data(self):
        print(self.df.tail)
