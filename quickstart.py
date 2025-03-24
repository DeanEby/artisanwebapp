import os.path
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
token_path = "secrets/token.json"
credentials_path = "secrets/credentials.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_messages(service, user_id):
  try:
    return service.users().messages().list(userId=user_id).execute()
  except Exception as error:
    print('An error occured: %s' % error)

def get_message(service, user_id, msg_id):
  try:
    return service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
  except Exception as error:
    print('An error occured: %s' % error)

def get_mime_message(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
    mime_msg = email.message_from_string(msg_str)
    return mime_msg
  except Exception as error:
    print('An error occured: %s' % error)

def get_attachments(service, user_id, msg_id, store_dir):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    for part in message['payload']['parts']:
      if(part['filename'] and part['body'] and part['body']['attachmentId']):
        attachment = service.users().messages().attachments().get(id=part['body']['attachmentId'], userId=user_id, messageId=msg_id).execute()
        file_data = base64.urlsafe_b64decode(attachment['data'].encode('utf-8'))
        path = ''.join([store_dir, part['filename']])
        return file_data
  except Exception as error:
    print('An error occured: %s' % error)

def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credentials_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  messages = get_messages(service, "me")

  message1 = messages['messages'][0]['id']
  print(get_attachments(service, "me", message1, ''))


if __name__ == "__main__":
  main()