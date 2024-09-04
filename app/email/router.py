import http.client
from wsgiref import headers
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_async_session
from app.email.schema import *
from app.email.models import TempEmail as TempEmail_model
from app.email.functions import *
from app.crud_manager import *


router = APIRouter(tags=["Email"])

MAILSAC_API_KEY = settings.MAILSAC_KEY
MAILSAC_BASE_URL = settings.MAILSAC_BASE_URL

MAILGUN_API_KEY = settings.MAILGUN_API_KEY
MAILGUN_BASE_URL = settings.MAILGUN_BASE_URL
MAILGUN_CUSTOM_DOMAIN = settings.MAILGUN_CUSTOM_DOMAIN
MAILGUN_API_URL = settings.MAILGUN_API_URL


@router.get("/addresses/{email}/messages")
async def list_messages_for_an_email(email):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/addresses/{email}/messages", headers=headers)

        res = conn.getresponse()
        data = res.read()
        parsed_json = json.loads(data.decode("utf-8"))

        return parsed_json
    except Exception as e:
        return {"error": f"Failed to get a list of messages for {email}. {e}"}


@router.get("/body/{email}/{message_id}")
async def get_message_html_body_no_links(email, message_id):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/body/{email}/{message_id}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return {"error": f"Failed to get sanitazed html body for {email}. {e}"}


@router.get("/dirty/{email}/{message_id}")
async def get_message_html_body_with_links(email, message_id):
    try:
        conn = http.client.HTTPSConnection("mailsac.com")
        headers = {"Mailsac-Key": MAILSAC_API_KEY}
        conn.request("GET", f"/api/dirty/{email}/{message_id}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
    except Exception as e:
        return {"error": f"Failed to get dirty html body for {email}. {e}"}


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
        parsed_json = json.loads(data.decode("utf-8"))

        return parsed_json
    except Exception as e:
        return {"error": f"Failed to get metadata for {email}. {e}"}


@router.get("/addresses/{email}/messages/{message_id}/formatted_json")
async def get_formatted_email_metadata(email, message_id):
    try:
        metadata = await get_email_metadata(email, message_id)
        formatted_metadata = {
            "message_id": metadata["_id"],
            "from_name": metadata["from"][0]["name"],
            "from_address": metadata["from"][0]["address"],
            "from_domain": metadata["domain"],
            "subject": metadata["subject"],
            "date_received": metadata["received"],
            "links": metadata["links"],
        }
        return formatted_metadata
    except Exception as e:
        return {"error": f"Failed to format original metadata for {email}. {e}"}


@router.post("/create")
async def create_temp_email(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        temp_email = await create_mailsac_public_email()
        await service_add_model(temp_email, session)
        await session.commit()
        return {
            "status": 201,
            "data": {
                "message": f"Temp email was created: {temp_email.email}",
                "temp_email": temp_email.email,
                "temp_email_id": temp_email.id,
            },
        }
    except Exception as e:
        return {"error": f"Failed to create a temp email. {e}"}


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
        return {
            "error": f"Failed to get a temp email {temp_email.email} with id:{temp_email_id}. {e}"
        }


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
        return {
            "error": f"Failed to update temp email {temp_email.email} with id:{temp_email_id}. {e}"
        }


@router.delete("/delete/{temp_email_id}")
async def delete_temp_email(
    temp_email_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await service_delete_model(TempEmail_model, temp_email_id, session)
        await session.commit()
        return {"status": 204, "data": "Temp email is deleted"}
    except Exception as e:
        return {"error": f"Failed to delete a temp email with id:{temp_email_id}. {e}"}


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
        return {"error": f"Failed to get temp emails. {e}"}
