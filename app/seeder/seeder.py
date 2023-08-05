from math import e
from sqlalchemy.orm import Session
#from sqlalchemyseed import load_entities_from_json
#from sqlalchemyseed import load_entities_from_yaml
from sqlalchemyseed import load_entities_from_csv
from sqlalchemyseed import Seeder
from app.auth.models import Role,User

from app.models import *

#Reading from YAML/JSON is not possible due to the "Model not found exception"
#entities = load_entities_from_json('seeder_json/users.json')
#entities = load_entities_from_yaml('seeder_json/users.yaml')

def does_data_exist(db: Session, data: dict, model) -> bool:
    role_quantity = db.query(model).count()
    if role_quantity < len(data):
        return False
    return True

def create_table(db: Session, path_to_file, model):

    entities = load_entities_from_csv(path_to_file, model)
    entities["data"] = cast_to_int(entities["data"])
    
    does_exist = does_data_exist(db, entities, model)
    if not does_exist:
        seeder = Seeder(db)
        seeder.seed(entities)
        db.commit()
    pass

def cast_to_int(entities):
    for i, object in enumerate(entities):
        for key in object:
            if key.endswith("id"):
                object[key] = int(object[key])
        entities[i] = object

    return entities

def seed(engine):
    db = Session(bind=engine)
    try:
        create_table(db, "seeder_files/roles.csv", Role)
        create_table(db, "seeder_files/users.csv", User)
        create_table(db, "seeder_files/temp_emails.csv", Temp_Email)
        create_table(db, "seeder_files/categories.csv", Category)
        create_table(db, "seeder_files/applications.csv", Application)
        create_table(db, "seeder_files/message_types.csv", Message_Type)
        create_table(db, "seeder_files/messages.csv", Message)
    finally:
        db.close()
    pass