from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_async_session
from app.application.model import Application
from app.application.schema import Application as ApplicationSchema


def service_add_application(
    category_id: int,
    website_url: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_application = Application(
        category_id=category_id, website_url=website_url
    )
    session.add(new_application)
    session.commit()
    return new_application