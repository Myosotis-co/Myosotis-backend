import random
import string


class Email:
    @staticmethod
    def generate_random_email_prefix(size, chars):
        random_email_prefix = ''.join(random.choice(chars) for _ in range(size))
        return random_email_prefix

    @staticmethod
    def generate_specific_email_prefix():
        specific_email_prefix = input("What is your new email? Press enter if you want random.    ")
        return specific_email_prefix

    @staticmethod
    def generate_email_prefix():
        email_prefix = Email.generate_specific_email_prefix()
        if email_prefix == "":
            return Email.generate_random_email_prefix(size=10, chars=string.ascii_lowercase + string.digits)
        else:
            return email_prefix
