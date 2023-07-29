from app.database import Base

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData,text
from sqlalchemy.orm import relationship
from app.models import Category
metadata = MetaData()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    name = Column(String)
    email = Column(String, unique=True)
    user_token = Column(String, unique=True)
    hashed_password = Column(String)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    categories = relationship(Category, backref='categories', passive_deletes=True)