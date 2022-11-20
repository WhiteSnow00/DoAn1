from __future__ import print_function

from snippets.get_token import get_token
# from get_token import get_token

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def append_values(spreadsheet_id, range_name, values):
    """
    Creates the batch_update the user has access to.
    """
    creds = get_token(SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the sheets API
        result = service.spreadsheets().values().append(
            spreadsheetId = spreadsheet_id,
            range = range_name,
            valueInputOption = 'USER_ENTERED',
            body = { 'values': values }
        ).execute()
        updatedCells = result.get('updates').get('updatedCells')
        print(f"{updatedCells} cells appended.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: spreadsheet_id, range_name, values
    append_values(
        "1woHLQaJU4PKlurYx2cT0k89pXVCRQBN0Hwr1rxgAUQI",
        "Sach!A1:I1000",
        [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        ]
    )