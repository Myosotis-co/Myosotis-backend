from sqlalchemy.orm import Session
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import load_entities_from_yaml
from sqlalchemyseed import load_entities_from_csv
from sqlalchemyseed import Seeder
import sqlalchemy as sa
from alembic import op

from app.models import *

# Reading from YAML/JSON is not possible due to the "Model not found exception"
#entities = load_entities_from_json('seeder_json/users.json')
#entities = load_entities_from_yaml('seeder_json/users.yaml')

def create_roles(db: Session):
    print('Creating roles...')
    entities = load_entities_from_csv('seeder_files/roles.csv', Role)
    does_exist = does_data_exist(db, entities)
    if not does_exist:
        seeder = Seeder(db)
        seeder.seed(entities)
        db.commit()
    pass

def does_data_exist(db: Session, data: dict) -> bool:
    role_quantity = db.query(Role).count()
    if role_quantity < len(data):
        return False
    return True

def create_users(db: Session):
    entities = load_entities_from_csv('seeder_json/users.csv', User)
    seeder = Seeder(db)
    seeder.seed(entities)
    db.commit()
    pass

def seed(engine):
    db = Session(bind=engine)

	# Session.configure(bind=op.get_bind())
	# db = Session()

    # engine = op.get_db().engine
    # db = engine.connect()

    try:
        create_roles(db)
        create_users(db)
    finally:
        db.close()
    pass