import string
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from spreadsheet import Spreadsheet

class Classifier:
    """Uses sklearn, pandas, and Naive Bayes to predict if certain text belongs to one of two labels"""

    __nb = MultinomialNB()
    __vectorizer = CountVectorizer()
    __encoder = LabelEncoder()
    __x_train, __x_test, __y_train, __y_test = None, None, None, None

    def __init__(self, spreadsheet:Spreadsheet):
        self.df = self.__get_dataset(spreadsheet=spreadsheet)

        self.__setup()

    def __setup(self):
        """clean data set & fit sample data"""

        self.__clean_data()
        self.__fit()

    def __get_dataset(self, spreadsheet:Spreadsheet) -> DataFrame:
        """retrieve most recent dataset using a spreadsheet name and sheet

            Parameters
            ----------
            sheet_name: str
                The parent sheet name the google account has access too
            sheet_page: str
                The specific sheet page with the `sheet_name`

            Returns
            --------
            DataFrame
                Pandas-generated DataFrame using specified sheet
        """

        data_sheet = spreadsheet.sheet
        rows = data_sheet.get_all_values()
        return pd.DataFrame.from_records(rows)

    
    def __clean_data(self):
        """
        Removes punctuation, HTML, from first column in data set\n
        - df[0] is first column, df[1] is second column
        """

        try:
            self.df[0] = self.df[0].apply(lambda x: x.lower())
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', '\n')))
            print('Successfully cleaned data.')
        except AttributeError as e:
            print(f'Whoops: {repr(e)}')

    def __fit(self):
        """fit data using Naive Bayes classifier"""

        # pull data into vectors to create collection of text/tokens
        x = self.__vectorizer.fit_transform(self.df[0])
        y = self.__encoder.fit_transform(self.df[1])

        # split into train and test sets
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=0.2)

        # Fit dataset in naive bayes classifier
        self.__nb.fit(self.__x_train, self.__y_train)

    def predict(self, text:str, correct_label, wrong_label):
        """Predict the category the given `text` belongs to

            Parameters
            ----------
            correct_label:str
                One of two categories the text can belong too
            wrong_label:str
                One of two categories the text can belong too

            Returns
            -------
            prediction:str
                Either `correct_label` or `wrong_label`
        """
        category_names = {correct_label: correct_label, wrong_label: wrong_label}
        cod = self.__nb.predict(self.__vectorizer.transform([text]))
        return category_names[self.__encoder.inverse_transform(cod)[0]]
