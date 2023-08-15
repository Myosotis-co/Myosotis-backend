# from app.email.functions import Email
import http.client
from fastapi import APIRouter

router = APIRouter(tags=["Email"])

MAILSAC_API_KEY = "insert_key_here"
MAILSAC_BASE_URL = "mailsac.com"


# email = Email.generate_email_prefix() + "@mailsac.com"


@router.get("/check-email-availability/{email}")
async def check_email_availability(email):
    try:
        conn = http.client.HTTPSConnection(MAILSAC_BASE_URL)
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/addresses/{email}/availability", headers=headers)

        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to check email availability: {e}"


@router.get("/validations/addresses/{email}")
async def validate_user_login_email(email):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/validations/addresses/{email}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to validate email: {e}"


@router.get("/addresses/{email}/messages")
async def list_messages_for_an_email(email):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/addresses/{email}/messages", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to get a list of messages for email: {e}"


@router.get("/raw/{email}/{message_id}")
async def get_original_email_message(email, message_id):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/raw/{email}/{message_id}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to get SMTP for email: {e}"


@router.get("/addresses/{email}/messages/{message_id}")
async def get_email_metadata(email, message_id):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request(
            "GET", f"/api/addresses/{email}/messages/{message_id}", headers=headers
        )

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to get metadata for email: {e}"


@router.get("/text/{email}/{message_id}")
async def get_email_message(email, message_id):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/text/{email}/{message_id}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to get message for email: {e}"
