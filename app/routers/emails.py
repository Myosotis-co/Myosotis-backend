from app.functions.initialize_email import Email
import http.client
from fastapi import APIRouter

router = APIRouter()

MAILSAC_API_KEY = ""
MAILSAC_BASE_URL = "mailsac.com"
email = Email.generate_email_prefix() + "@mailsac.com"


@router.get("/check-email-availability/{email}")
async def check_email_availability(email):
    try:
        conn = http.client.HTTPSConnection(MAILSAC_BASE_URL)
        headers = {'Mailsac-Key': MAILSAC_API_KEY}
        conn.request("GET", f"/api/addresses/{email}/availability", headers=headers)

        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    except Exception as e:
        return f"Failed to check email availability: {e}"


@router.get("/validations/addresses/{email}")
async def validate_user_login_email(login_email):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {'Mailsac-Key': MAILSAC_API_KEY}

        conn.request("GET", "/api/validations/addresses/{login_email}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
    except Exception as e:
        return f"Failed to validate email: {e}"
