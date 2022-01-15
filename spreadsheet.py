import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Spreadsheet:
    """
    Uses Google Drive API to authorize a session for a Google Service account\n
    Allows the opening of sheets from a spreadsheets session
    """

    _scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # define the scope
    _credentials = ServiceAccountCredentials.from_json_keyfile_name('google_key.json', _scope)  # account credentials
    _client = gspread.authorize(_credentials)  # authorize clientsheet

    sheet = None  # Specific sheet in CSV file

    def __init__(self, sheet_name, sheet_page):
        self.set_current_sheet(sheet_name=sheet_name, sheet_page=sheet_page)

    def set_current_sheet(self, sheet_name, sheet_page):
        """
        Open spreadsheet for editing and parsing

        Parameters
        ----------
        sheet_name: str
            The parent sheet name the google account has access too
        sheet_page: str
            The specific sheet page with the `sheet_name`
        """
        try:
            self.sheet = self._client.open(sheet_name).worksheet(sheet_page)
            print(f'Opened sheet: {sheet_name}')
        except gspread.SpreadsheetNotFound:
            print(f'Spreadsheet {sheet_page} with sheet: {sheet_name} does not exist.')
