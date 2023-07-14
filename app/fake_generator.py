from faker import Faker
from datetime import datetime

fake = Faker()

def generate_fake_users(num_users):
    users = []
    for i in range(num_users):
        user = {
            'name': fake.name(),
            'email': fake.email(),
            'user_token': "not_real_token" + str(i),
            'hashed_password': 'hashed_not_real_password' + str(i)
        }
        users.append(user)
    return users