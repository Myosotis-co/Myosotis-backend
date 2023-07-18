from venv import create
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey,MetaData, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    name = Column(String)
    email = Column(String, unique=True)
    user_token = Column(String)
    hashed_password = Column(String)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))