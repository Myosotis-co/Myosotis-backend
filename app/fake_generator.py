

from faker import Faker
from datetime import datetime
fake = Faker()

def generate_fake_landmarks(num_landmarks,user_id):
    landmarks = []
    for i in range(num_landmarks):
        landmark = {
            'name': "Landmark" + str(i),
            'description': "Nice landmark" + str(i),
            'latitude': fake.latitude(),
            'longitude': fake.longitude(),
            'user_id': user_id,
            'image': fake.image_url(),
            'created_at': datetime.now()
        }
        landmarks.append(landmark)
    return landmarks


def generate_fake_users(num_users):
    users = []
    for i in range(num_users):
        user = {
            'name': fake.name(),
            'email': fake.email(),
            'created_at': str(datetime.now()),
            'hashed_password': 'hashed_not_real_password' + str(i)
        }
        users.append(user)
    return users

def generate_fake_routers(num_routes,user_id):
    routes = []
    for i in range(num_routes):
        route = {
            'name': "Route" + str(i),
            'description': "Nice route" + str(i),
            'user_id': user_id,
            'created_at': str(datetime.now())
        }
        routes.append(route)
    return routes