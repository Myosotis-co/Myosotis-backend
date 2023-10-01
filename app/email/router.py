import http.client
import json
from app.config import settings
from fastapi import APIRouter
from app.email.functions import generate_random_mailsac_email

router = APIRouter(tags=["Email"])

MAILSAC_API_KEY = settings.MAILSAC_KEY
MAILSAC_BASE_URL = settings.MAILSAC_BASE_URL


async def check_generated_temp_email():
    is_owned = True
    mailsac_temp_email = ""
    while is_owned:
        mailsac_temp_email = generate_random_mailsac_email()
        response_data = await check_email_availability(mailsac_temp_email)
        response_json = json.loads(response_data)
        is_owned = response_json["owned"]
    return mailsac_temp_email


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


@router.get("/addresses/{email}")
async def create_mailsac_public_email():
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        email = await check_generated_temp_email()

        conn.request("GET", f"/api/addresses/{email}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to fetch email: {e}"


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
