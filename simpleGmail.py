from simplegmail import Gmail
import re

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


gmail = Gmail('secrets/credentials.json')

def cleanMessageHTML(message):
    regex = re.compile('<.*?>')
    message = message.replace('</td>', '##SPLIT##')
    message = message.replace(':', '')
    message = re.sub(regex, '', message)
    message = message.replace('\n', '')
    message = message.replace('\r', ' ')
    return message


def getUnreadMessagesAsDict(gmail):
    messages = gmail.get_unread_inbox()
    all_messages_list = []
    for message in messages:
        message_html = cleanMessageHTML(message.html)
        message_list = message_html.split('##SPLIT##')
        message_list = [line for line in message_list if line]
        all_messages_list.append(message_list)

    message_dict_list = []
    for message in all_messages_list:
        message_dict = {}
        for index, item in enumerate(message):
            if index % 2 == 0:
                if index < len(message) -1:
                    message_dict[item] = message[index + 1]
        message_dict_list.append(message_dict)

        
    return message_dict_list
    
output = getUnreadMessagesAsDict(gmail)

print(output)




# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A2:E"



import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A2:E"


def sheetsTest():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("secrets/token.json"):
    creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "secrets/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("secrets/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    with open("secrets/spreadsheetid.txt", "r") as file:
       spreadsheet_id = file.read()
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range="Sheet1!A1:L14")
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    print("Name, Major:")
    for row in values:
      # Print columns A and E, which correspond to indices 0 and 4.
      print(f"{row[0]}, {row[4]}")
  except HttpError as err:
    print(err)

sheetsTest()