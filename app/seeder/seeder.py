from sqlalchemy.future import select
from app.database import get_async_session
from app.auth.models import Role, User
from app.category.models import Category
from app.email.models import TempEmail
from app.application.models import Application
from app.models import *
from sqlalchemyseed import load_entities_from_csv, Seeder
import sqlalchemy as sa

from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext


async def does_data_exist(db, data, model):
    element = await db.execute(select(model))
    role_quantity = len(element.scalars().all())
    if role_quantity < len(data):
        return False
    return True


async def create_table(db, path_to_file, model):
    entities = load_entities_from_csv(path_to_file, model)
    entities["data"] = cast_to_int(entities["data"])
    entities["data"] = hash_password(entities["data"])

    does_exist = await does_data_exist(db, entities, model)
    if not does_exist:
        seeder = Seeder(db)
        seeder.seed(entities)
        await db.commit()


def cast_to_int(entities):
    for i, obj in enumerate(entities):
        for key in obj:
            if key.endswith("id"):
                obj[key] = int(obj[key])
        entities[i] = obj
    return entities


def hash_password(entities):
    for i, obj in enumerate(entities):
        for key in obj:
            if key.endswith("hashed_password"):
                context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                password_helper = PasswordHelper(context)
                obj[key] = password_helper.hash(obj[key])
        entities[i] = obj
    return entities


async def seed(db):
    await create_table(db, "seeder_files/roles.csv", Role)
    await create_table(db, "seeder_files/users.csv", User)
    await create_table(db, "seeder_files/temp_emails.csv", TempEmail)
    await create_table(db, "seeder_files/categories.csv", Category)
    await create_table(db, "seeder_files/applications.csv", Application)
    await create_table(db, "seeder_files/message_types.csv", Message_Type)
    await create_table(db, "seeder_files/messages.csv", Message)
