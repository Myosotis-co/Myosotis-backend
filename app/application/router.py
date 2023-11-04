from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.application.schema import *
from app.application.models import Application as Application_model
from app.crud_manager import *

router = APIRouter(tags=["Application"])


@router.post("/create")
async def create_application(
    application_create: ApplicationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await service_create_model(Application_model, application_create, session)
    try:
        await session.commit()
        return {"status": 201, "data": "Application is created"}
    except Exception as e:
        return "Failed to create application: " + str(e)


@router.get("/get/{category_id}")
async def get_application(
    application_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        application = await service_get_model(
            Application_model, application_id, session
        )
        if application is not None:
            return application
        raise HTTPException(status_code=404, detail="Applicaion not found")
    except Exception as e:
        return "Failed to get an applicaion: " + str(e)


@router.patch("/update/{application_id}")
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        application = await service_get_model(
            Application_model, application_id, session
        )
        if application is not None:
            await service_update_model(application, application_update, session)
            await session.commit()
            return {"status": 204, "data": "Application is updated"}
        raise HTTPException(status_code=404, detail="Application not found")
    except Exception as e:
        return "Failed to update an application: " + str(e)


@router.delete("/delete/{application_id}")
async def delete_application(
    application_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await service_delete_model(Application_model, application_id, session)
        await session.commit()
        return {"status": 204, "data": "Application is deleted"}
    except Exception as e:
        return "Failed to delete an application: " + str(e)


@router.get("/get_all")
async def get_applications(
    page_num: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        applications = await service_get_some_models(
            Application_model, page_num, items_per_page, session
        )
        return applications
    except Exception as e:
        return "Failed to get applications: " + str(e)
