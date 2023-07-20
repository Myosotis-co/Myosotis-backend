from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, MetaData, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    message_type_id = Column(Integer, ForeignKey("message_types.id"))
    topic = Column(String)
    message_text = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Message_Type(Base):
    __tablename__ = "message_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    messages = relationship(Message, backref='messages', passive_deletes=True)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    website_url = Column(String)
    deletion_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    received_messages = relationship(Message, backref='received_messages', passive_deletes=True)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    temp_email_id = Column(Integer, ForeignKey("temp_emails.id"))
    category_name = Column(String)
    deletion_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    applications = relationship(Application, backref='applications', passive_deletes=True)
    temp_email = relationship("Temp_Email", back_populates="category", passive_deletes=True)

class Temp_Email(Base):
    __tablename__ = "temp_emails"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    access_token = Column(String, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    category = relationship(Category, back_populates="temp_email", passive_deletes=True) 

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

    users = relationship(User, backref='users', passive_deletes=True)
