import random
import string

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.email.models import Temp_Email
from app.email.schema import Temp_Email


def generate_random_mailsac_email():
    random_prefix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )
    mailsac_temp_email = random_prefix + "@mailsac.com"
    return mailsac_temp_email


def service_add_temp_email(
    id: int,
    email: str,
    access_token: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_temp_email = Temp_Email(id=id, email=email, access_token=access_token)
    session.add(new_temp_email)
    session.commit()
    return new_temp_email
