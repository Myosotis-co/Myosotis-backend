from sqlalchemy.orm import Session
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder
from app.database import SessionLocal

def create_roles(db: Session):
    entities = load_entities_from_json('seeder_json/roles.json')
    seeder = Seeder(db)
    seeder.seed(entities)
    db.commit()
    pass

def seed():
    db = SessionLocal()
    try:
        create_roles(db)
    finally:
        db.close() 
    pass