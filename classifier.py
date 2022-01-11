import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from spreadsheet import Spreadsheet

# Uses sklearn, pandas, and Naive Bayes to predict if certain text belongs to one of two labels
class Classifier:
    __nb = MultinomialNB()
    __vectorizer = CountVectorizer()
    __encoder = LabelEncoder()
    __x_train, __x_test, __y_train, __y_test = None, None, None, None

    def __init__(self, sheet_name, sheet_page):
        self.sheet_name = sheet_name
        self.sheet_page = sheet_page
        self.df = self.__get_dataset(sheet_name, sheet_page)

        self.__setup()

    # clean data set & fit sample data
    def __setup(self):
        self.clean_data()
        self.fit()

    # Retrieve most recent dataset using a spreadsheet
    def __get_dataset(self, sheet_name, sheet_page):
        data_sheet = Spreadsheet(sheet_name, sheet_page).sheet
        rows = data_sheet.get_all_values()
        return pd.DataFrame.from_records(rows)

    # Removes punctuation, HTML, from EMAIL column in data set
    # df[0] is first column, df[1] is second column
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
        x = self.__vectorizer.fit_transform(self.df[0])
        y = self.__encoder.fit_transform(self.df[1])

        # split into train and test sets
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=0.2)

        # Fit dataset in naive bayes classifier
        self.__nb.fit(self.__x_train, self.__y_train)

    # Predict if @param email is apart of specific column or not
    def predict(self, email, correct_label, wrong_label):
        category_names = {correct_label: correct_label, wrong_label: wrong_label}
        cod = self.__nb.predict(self.__vectorizer.transform([email]))
        return category_names[self.__encoder.inverse_transform(cod)[0]]
