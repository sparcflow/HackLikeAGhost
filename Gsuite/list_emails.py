from googleapiclient import discovery
from httplib2 import Http
import json
from base64 import b64decode
from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]

# Service account file with wide delegation
SERVICE_ACCOUNT_FILE = "token.json"
# The user we want to "impersonate"
USER_EMAIL = "admin@example.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
delegated_credentials = credentials.with_subject(USER_EMAIL)

service = discovery.build("gmail", "v1", credentials=delegated_credentials)
results = (
    service.users().messages().list(userId=USER_EMAIL, labelIds=["INBOX"]).execute()
)

messages = results.get("messages", [])

for message in messages:
    msg = service.users().messages().get(userId=USER_EMAIL, id=message["id"]).execute()
    for header in msg["payload"]["headers"]:
        if header["name"] == "Delivered-To":
            emailFrom = header["value"]
        if header["name"] == "To":
            emailTo = header["value"]
        if header["name"] == "Date":
            emailDate = header["value"]
        if header["name"] == "Subject":
            subject = header["value"]
    text = msg["payload"]["parts"][0]["body"]["data"]
    try:
        print(emailFrom, emailTo, emailDate, subject)
        print(b64decode(text).decode())
        print("--")
    except:
        pass

