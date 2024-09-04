import base64
import http.client
import urllib.parse

from starlette.responses import JSONResponse
from wsgiref import headers
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.email.schema import *
from app.email.functions import *
from app.crud_manager import *

router = APIRouter(tags=["Mailgun"])

MAILSAC_API_KEY = settings.MAILSAC_KEY
MAILSAC_BASE_URL = settings.MAILSAC_BASE_URL

MAILGUN_API_KEY = settings.MAILGUN_API_KEY
MAILGUN_BASE_URL = settings.MAILGUN_BASE_URL
MAILGUN_CUSTOM_DOMAIN = settings.MAILGUN_CUSTOM_DOMAIN
MAILGUN_API_URL = settings.MAILGUN_API_URL


@router.post("/email_single_send")
async def send_single_email(
    message: str, email: str, context: str, subject: str
) -> JSONResponse:
    try:
        html = f"<p>{message}</p>" + context
        conn = http.client.HTTPSConnection(MAILGUN_BASE_URL)
        api_key = "api:" + MAILGUN_API_KEY
        user_and_pass = base64.b64encode(api_key.encode()).decode("ascii")

        headers = {
            "Authorization": "Basic " + user_and_pass,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = urllib.parse.urlencode(
            {
                "from": f"Myosotis support <notification@{MAILGUN_CUSTOM_DOMAIN}>",
                "to": email,
                "subject": subject,
                "html": html,
            }
        )
        conn.request("POST", MAILGUN_API_URL, body=data, headers=headers)
        print(conn.getresponse().read().decode("utf-8"))
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        return f"Failed to send message {email}: {e}"
