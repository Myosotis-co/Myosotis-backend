from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.application.schema import *
from app.application.functions import *

router = APIRouter(tags=["Application"])


@router.post("/applications/create")
async def create_applications(
    category_id: int,
    website_url: str,
    session: AsyncSession = Depends(get_async_session),
):
    service_add_application(category_id, website_url, session)
    try:
        await session.commit()
        return {"status": 201, "data": "Application is created"}
    except Exception as e:
        return "Failed to create application: " + str(e)


@router.get("/applications/get/{category_id}")
async def get_application(
    application_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        application = await service_get_application(application_id, session)
        if application is not None:
            return application
        raise HTTPException(status_code=404, detail="Applicaion not found")
    except Exception as e:
        return "Failed to get an applicaion: " + str(e)


@router.patch("/applications/update/{application_id}")
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        application = await service_get_application(application_id, session)
        if application is not None:
            service_update_application(application, application_update, session)
            await session.commit()
            return {"status": 204, "data": "Application is updates"}
        raise HTTPException(status_code=404, detail="Application not found")
    except Exception as e:
        return "Failed to update an application" + str(e)


@router.delete("/applications/delete/{application_id}")
async def delete_application(
    application_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await service_delete_application(application_id, session)
        await session.commit()
        return {"status": 204, "data": "Application is deleted"}
    except Exception as e:
        return "Failed to delete an application" + str(e)


@router.get("applications/get_all")
async def get_applications(session: AsyncSession = Depends(get_async_session)):
    applications = await service_get_applications(session)
    return applications