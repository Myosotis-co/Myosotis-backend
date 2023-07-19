from venv import create
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey,MetaData, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.User import User

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    users = relationship(User, backref='user', passive_deletes=True)