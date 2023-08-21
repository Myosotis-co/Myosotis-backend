import json
import random
import string
from app.email.router import check_email_availability, create_mailsac_public_email


def generate_random_email_prefix(size, chars):
    random_email_prefix = "".join(random.choice(chars) for _ in range(size))
    return random_email_prefix


async def create_mailsac_temp_email():
    is_owned = True
    mailsac_temp_email = ""
    while is_owned:
        mailsac_temp_email = (
            generate_random_email_prefix(
                size=10, chars=string.ascii_lowercase + string.digits
            )
            + "@mailsac.com"
        )
        response_data = await check_email_availability(mailsac_temp_email)
        response_json = json.loads(response_data)
        is_owned = response_json["owned"]

    await create_mailsac_public_email(mailsac_temp_email)
    return mailsac_temp_email
