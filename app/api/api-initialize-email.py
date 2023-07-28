import random
import string
import http.client


def generate_random_email_prefix(size, chars):
    random_email_prefix = ''.join(random.choice(chars) for _ in range(size))
    return random_email_prefix


def generate_specific_email_prefix():
    specific_email_prefix = input("What is your new email? Press enter if you want random.    ")
    return specific_email_prefix


def generate_email_prefix():
    email_prefix = generate_specific_email_prefix()
    if email_prefix == "":
        return generate_random_email_prefix(size=10, chars=string.ascii_lowercase + string.digits)
    else:
        return email_prefix


email = generate_email_prefix() + "@mailsac.com"
conn = http.client.HTTPSConnection("mailsac.com")

headers = {'Mailsac-Key': "k_M0F13in1d4DgPcxg3EF5O0qGW6lVdrP5qszxRZM7f"}

conn.request("GET", f"/api/addresses/{email}/availability", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
