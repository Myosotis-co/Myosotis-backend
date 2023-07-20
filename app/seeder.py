from sqlalchemy.orm import Session
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import load_entities_from_yaml
from sqlalchemyseed import load_entities_from_csv
from sqlalchemyseed import Seeder
from app.database import SessionLocal
from app.models import Role

# Reading from YAML/JSON is not possible due to the "Model not found exception"
#entities = load_entities_from_json('seeder_json/users.json')
#entities = load_entities_from_yaml('seeder_json/users.yaml')

def create_roles(db: Session):
    entities = load_entities_from_csv('seeder_files/roles.csv', Role)
    does_exist = does_roles_exist(db, entities)
    if not does_exist:
        seeder = Seeder(db)
        seeder.seed(entities)
        db.commit()
    pass

def does_roles_exist(db: Session, roles: dict) -> bool:
    # I am stupid, how to do it properly?
    role_quantity = db.query(Role).count()
    if role_quantity < 2:
        return False
    return True

def seed():
    db = SessionLocal()
    try:
        create_roles(db)
    finally:
        db.close()
    pass