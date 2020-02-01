from googleapiclient import discovery
from httplib2 import Http
import json, sys
from base64 import b64decode
from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
]

## To Update ##
SERVICE_ACCOUNT_FILE = "token.json"
ADMIN_EMAIL = "admin@example.com"
USER_EMAIL = "user@example.com"
## End ##

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
delegated_credentials = credentials.with_subject(ADMIN_EMAIL)
service = discovery.build("admin", "directory_v1", credentials=delegated_credentials)
user = {
    "name": {"familyName": "Burton", "givenName": "Haniel",},
    "password": "Random76Pass_",
    "primaryEmail": USER_EMAIL,
    "orgUnitPath": "/",
}
service.users().insert(body=user).execute()
result = (
    service.users()
    .makeAdmin(userKey=user["primaryEmail"], body={"status": True})
    .execute()
)
