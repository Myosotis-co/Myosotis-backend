import http.client
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_async_session
from app.email.schema import *
from app.email.models import TempEmail as TempEmail_model
from app.email.functions import *
from app.crud_manager import *

from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

router = APIRouter(tags=["Email"])

MAILSAC_API_KEY = settings.MAILSAC_KEY
MAILSAC_BASE_URL = settings.MAILSAC_BASE_URL


conf = ConnectionConfig(
    MAIL_USERNAME = "SENDER EMAIL", #Ask for config
    MAIL_PASSWORD = "GOD SUPER SECURE PASSWORD",  #Need to do 2 step verification to work
    MAIL_FROM = "SENDER EMAIL",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
)

@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    try:
        html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=email.dict().get("email"),
            body=html,
            subtype=MessageType.html)

        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        return f"Failed to send message {email}: {e}"

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
        return f"Failed to get a list of messages for {email}: {e}"


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
        return f"Failed to get SMTP for {email}: {e}"


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
        return f"Failed to get metadata for {email}: {e}"


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
        return f"Failed to get message for {email}: {e}"


@router.post("/create")
async def create_temp_email(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        temp_email = await create_mailsac_public_email()
        await service_add_model(temp_email, session)
        await session.commit()
        return {"status": 201, "data": f"Temp email was created: {temp_email.email}"}
    except Exception as e:
        return "Failed to create a temp email: " + str(e)


@router.get("/get/{temp_email_id}")
async def get_temp_email(
    temp_email_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        temp_email = await service_get_model(TempEmail_model, temp_email_id, session)
        if temp_email is not None:
            return temp_email
        raise HTTPException(
            status_code=404, detail=f"Temp email: {temp_email.email}  was not found"
        )
    except Exception as e:
        return "Failed to get a temp email: " + str(e)


@router.patch("/update/{temp_email_id}")
async def update_temp_email(
    temp_email_id: int,
    temp_email_update: TempEmailUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        temp_email = await service_get_model(TempEmail_model, temp_email_id, session)
        if temp_email is not None:
            await service_update_model(temp_email, temp_email_update, session)
            await session.commit()
            return {"status": 204, "data": "Temp email is updated"}
        raise HTTPException(
            status_code=404, detail=f"Temp email: {temp_email.email} is not found"
        )
    except Exception as e:
        return "Failed to update temp email: " + str(e)


@router.delete("/delete/{temp_email_id}")
async def delete_temp_email(
    temp_email_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await service_delete_model(TempEmail_model, temp_email_id, session)
        await session.commit()
        return {"status": 204, "data": "Temp email is deleted"}
    except Exception as e:
        return "Failed to delete a temp email: " + str(e)


@router.get("/get_all")
async def get_temp_emails(
    page_num: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        temp_emails = await service_get_some_models(
            TempEmail_model, page_num, items_per_page, session
        )
        return temp_emails
    except Exception as e:
        return "Failed to get temp emails: " + str(e)
