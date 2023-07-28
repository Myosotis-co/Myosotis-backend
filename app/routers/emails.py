from app.functions.initialize_email import Email
import http.client
from fastapi import APIRouter

emails = APIRouter()

MAILSAC_API_KEY = "k_M0F13in1d4DgPcxg3EF5O0qGW6lVdrP5qszxRZM7f"
MAILSAC_BASE_URL = "mailsac.com"
email = Email.generate_email_prefix() + "@mailsac.com"


@emails.get("/check-email-availability/{email}")
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
