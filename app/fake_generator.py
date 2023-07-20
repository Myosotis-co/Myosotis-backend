from faker import Faker
from datetime import datetime
from app.models.Role import Role

#fake = Faker()


"""
def generate_fake_users(num_users):
    db = SessionLocal()
    try:
        users = []
        for i in range(num_users):
            user = {
                'name': fake.name(),
                'email': fake.unique.email(),
                'role_id': db.query(Role).filter(Role.name == "User").first().id,
                'user_token': "not_real_token" + str(i),
                'hashed_password': 'hashed_not_real_password' + str(i)
            }
            users.append(user)
    finally:
        db.close()
    return users
"""