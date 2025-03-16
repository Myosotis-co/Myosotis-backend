import json
import requests
import os
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_google_access(code: str = None):

    if os.path.exists("token.json"):
        with open("token.json", "r") as token:
            return json.load(token)

    if not code:
        auth_data = get_credential_metadata()
        auth_uri = f"{auth_data['auth_uri']}?response_type=code&client_id={auth_data['client_id']}&redirect_uri=http://localhost:8000&scope={SCOPES[0]}"
        return auth_uri
    else:
        metadata = get_credential_metadata()
        token_request = {
            "code": code,
            "client_id": metadata["client_id"],
            "client_secret": metadata["client_secret"],
            "redirect_uri": "http://localhost:8000",
            "grant_type": "authorization_code",
        }
        try:
            r = requests.post("https://oauth2.googleapis.com/token", data=token_request)
            with open("token.json", "w") as token:
                token.write(r.text)
                token.close()
            return r.json()
        except Exception as e:
            return {"error": str(e)}


def get_credential_metadata():
    with open("app/gmail_api/credentials.json", "r") as f:
        auth_data = json.load(f)["web"]
        f.close()
        return auth_data


def create_credentials_object(metadata, access_response):
    google_creds_obj = Credentials(
        token=access_response,
        token_uri=metadata["token_uri"],
        client_id=metadata["client_id"],
        client_secret=metadata["client_secret"],
        scopes=SCOPES[0],
    )
    return google_creds_obj
