from googleapiclient import discovery
from httplib2 import Http
import json, sys, os
from base64 import b64decode
from google.oauth2 import service_account
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

MIMETYPES = {
    "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}
EXT = {
    "application/vnd.google-apps.document": ".docx",
    "application/vnd.google-apps.spreadsheet": ".xlsx",
    "application/vnd.google-apps.presentation": ".pptx",
}

SCOPES = [
    "https://www.googleapis.com/auth/drive",
]

## TO UPDATE ##
SERVICE_ACCOUNT_FILE = "token.json"
USER_EMAIL = "admin@example.com"
## END ##


def downloadFiles(drive, myfilter, outputDir):
    file_list = drive.ListFile({"q": myfilter}).GetList()
    for myfile in file_list:
        print("Downloading '%s', mime: '%s'" % (myfile["title"], myfile["mimeType"]))
        mimeType = MIMETYPES.get(myfile["mimeType"], myfile["mimeType"])
        ext = EXT.get(myfile["mimeType"], "")
        driveFile = drive.CreateFile({"id": myfile["id"]})
        driveFile.GetContentFile(
            "%s/%s%s" % (outputDir, myfile["title"], ext), mimetype=mimeType
        )


def connectDrive(service_account_file, user_email):
    gauth = GoogleAuth()
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        service_account_file, SCOPES
    )
    gauth.credentials = credentials.create_delegated(sub=USER_EMAIL)

    drive = GoogleDrive(gauth)
    return drive


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            """usage %s <filter> <output_dir>
        Filters found in https://developers.google.com/drive/api/v3/reference/query-ref
        Example: "title contains 'test'" """
            % sys.argv[0]
        )
        sys.exit(-1)

    myfilter = sys.argv[1]
    output = sys.argv[2]

    if not os.path.exists(output):
        os.makedirs(output)

    mydrive = connectDrive(SERVICE_ACCOUNT_FILE, USER_EMAIL)
    downloadFiles(mydrive, myfilter, output)
