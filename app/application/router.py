from app.auth.models import User
from app.permissions import check_user_access
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.application.schema import *
from app.application.models import Application as Application_model
from app.category.models import Category as Category_model
from app.crud_manager import *
from app.auth.jwt_config import fastapi_users

current_user = fastapi_users.current_user(active=True)
router = APIRouter(tags=["Application"], dependencies=[Depends(current_user)])


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
    application_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        application = await service_get_model(
            Application_model, application_id, session
        )
        if application is not None:
            if not check_user_access(user, application):
                return HTTPException(status_code=403, detail="Forbidden")
            return application
        return HTTPException(status_code=404, detail="Applicaion not found")
    except Exception as e:
        return "Failed to get an applicaion: " + str(e)


@router.patch("/update/{application_id}")
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        application = await service_get_model(
            Application_model, application_id, session
        )
        if application is not None:
            if not check_user_access(user, application):
                return HTTPException(status_code=403, detail="Forbidden")
            await service_update_model(application, application_update, session)
            await session.commit()
            return {"status": 204, "data": "Application is updated"}
        return HTTPException(status_code=404, detail="Application not found")
    except Exception as e:
        return "Failed to update an application: " + str(e)


@router.delete("/delete/{application_id}")
async def delete_application(
    application_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        application = await service_get_model(
            Application_model, application_id, session
        )
        if application is not None:
            if not check_user_access(user, application):
                return HTTPException(status_code=403, detail="Forbidden")
            await service_delete_model(Application_model, application_id, session)
            await session.commit()
            return {"status": 204, "data": "Application is deleted"}
        return HTTPException(status_code=404, detail="Application not found")
    except Exception as e:
        return "Failed to delete an application: " + str(e)


@router.get("/get_all")
async def get_applications(
    page_num: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        applications = await service_get_some_models(
            Application_model, page_num, items_per_page, session
        )
        applications = [
            application for application in applications if application is not None
        ]
        validatated_applications = []
        for application in applications:
            if check_user_access(user, application.Application):
                validatated_applications.append(application)

        return validatated_applications
    except Exception as e:
        return "Failed to get applications: " + str(e)
