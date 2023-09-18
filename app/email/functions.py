import random
import string


def generate_random_mailsac_email():
    random_prefix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )
    mailsac_temp_email = random_prefix + "@mailsac.com"
    return mailsac_temp_email

