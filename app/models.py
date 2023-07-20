from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey,MetaData, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    temp_email_id = Column(Integer, ForeignKey("temp_emails.id"))
    category_name = Column(String)
    deletion_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Temp_Email(Base):
    __tablename__ = "temp_emails"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    access_token = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    category = relationship(Category, backref='category', passive_deletes=True) 

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

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    users = relationship(User, backref='user', passive_deletes=True)
