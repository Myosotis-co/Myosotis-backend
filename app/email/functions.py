import string
import json
import random
import http.client
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_async_session
from app.config import settings
from app.email.schema import TempEmailCreate
from app.email.models import TempEmail as TempEmail_model

MAILSAC_API_KEY = settings.MAILSAC_KEY
MAILSAC_BASE_URL = settings.MAILSAC_BASE_URL


def generate_random_mailsac_email():
    random_prefix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )
    mailsac_temp_email = f"{random_prefix}@mailsac.com"
    return mailsac_temp_email


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


async def generate_valid_temp_email():
    is_owned = True
    mailsac_temp_email = ""
    while is_owned:
        mailsac_temp_email = generate_random_mailsac_email()
        response_data = await check_email_availability(mailsac_temp_email)
        response_json = json.loads(response_data)
        is_owned = response_json["owned"]
    return mailsac_temp_email


async def create_mailsac_public_email():
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        email = await generate_valid_temp_email()

        conn.request("GET", f"/api/addresses/{email}", headers=headers)

        temp_email_create = TempEmail_model(email=email, access_token=email)
        # temp_email_create = TempEmailCreate(email=email, access_token=email)

        return temp_email_create
    except Exception as e:
        return f"Failed to fetch email: {e}"
