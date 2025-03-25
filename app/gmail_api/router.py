from urllib.parse import unquote
from fastapi import APIRouter, Request
from app.gmail_api.api_access_utils import (
    create_credentials_object,
    get_credential_metadata,
    get_google_access,
)
from app.gmail_api.functions import gmail_get_formatted_messages, gmail_read_messages


router = APIRouter(tags=["DeveloperOnly"])


@router.get("/google_access")
def google_request_api(request: Request, code: str = None):
    try:
        response = get_google_access(unquote(code)) if code else get_google_access()
        request.session["google_token"] = response

        return {"status": 200, "data": response}

    except Exception as e:
        return "Failed to get a token: " + str(e)


@router.get("/gmail_read_message")
def google_read_message(request: Request, format: str = "minimal"):
    try:
        creds = create_credentials_object(
            get_credential_metadata(),
            request.session.get("google_token")["access_token"],
        )
        response = gmail_get_formatted_messages(creds, format)
        return {"status": 200, "messages": response}
    except Exception as e:
        return "Failed to get a message" + str(e)
