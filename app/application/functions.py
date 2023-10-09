from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_async_session
from app.application.models import Application
from app.application.schema import ApplicationUpdate
from app.application.schema import Application as ApplicationSchema


def service_add_application(
    category_id: int,
    website_url: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_application = Application(category_id=category_id, website_url=website_url)
    session.add(new_application)
    session.commit()
    return new_application


async def service_get_application(
    application_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = select(Application).filter(Application.id == application_id)
    result_value = await session.execute(exec_command)
    application = result_value.scalar()

    return application


def service_update_application(
    application: Application,
    application_update: ApplicationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    for key, value in application_update:
        if value is not None:
            setattr(application, key, value)
    session.add(application)
    return application


async def service_delete_application(
    application_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = delete(Application).filter(Application.id == application_id)
    await session.execute(exec_command)


async def service_get_applications(
    session: AsyncSession = Depends(get_async_session),
) -> list[ApplicationSchema]:
    exec_command = select(Application)
    result_value = await session.execute(exec_command)
    applications = result_value.all()

    return applications
