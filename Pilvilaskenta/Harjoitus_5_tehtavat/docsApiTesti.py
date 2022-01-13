#from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# The ID of a sample document.
# jotain tyyliin '12SDAGDg6h8dc9j5jukwlQ1-oVO2Af42ikvRggFfLQGuFG'
DOCUMENT_ID = '1bIjVJXf8HCHyfsinnTLh3U2eDxx5ARpaFPScFJDIols'


def main():
    """Shows basic usage of the Docs API.
    Prints title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_181376299240-1hotc6jqppt3703fho71sbk0iqpvj192.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    # tätä voi käyttää jos haluaa hakea jonku tietyn dokumentin
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    print('The title of the document is: {}'.format(document.get('title')))

    #tätä voi käyttää jos haluaa tehdä uuden dokumentin
    #title = 'Document created with Python123'
    #body = {
       # 'title': title
    #}
    #doc = service.documents() \
        #.create(body=body).execute()
    #print('Created document with title: {0}'.format(
        #doc.get('title')))

    requests = [
        {
            "insertTable":
                {
                    "rows": 2,
                    "columns": 2,
                    "location":
                        {
                            "index": 1
                        }
                }
        },
        {
            "insertText":
                {
                    "text": "Angelva",
                    "location":
                        {
                            "index": 12
                        }
                }
        },
        {
            "insertText":
                {
                    "text": "Noora",
                    "location":
                        {
                            "index": 10
                        }
                }
        },
        {
            "insertText":
                {
                    "text": "Sukunimi",
                    "location":
                        {
                            "index": 7
                        }
                }
        },
        {
            "insertText":
                {
                    "text": "Etunimi",
                    "location":
                        {
                            "index": 5
                        }
                }
        }
    ]

    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

if __name__ == '__main__':
    main()